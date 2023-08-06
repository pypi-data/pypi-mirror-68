//
// Copyright (C) 2018 by the adcc authors
//
// This file is part of adcc.
//
// adcc is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published
// by the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// adcc is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with adcc. If not, see <http://www.gnu.org/licenses/>.
//

#pragma once
#include "AdcMemory.hh"
#include "Symmetry.hh"
#include "adcc/config.hh"
#include "exceptions.hh"
#include <array>
#include <functional>
#include <memory>
#include <numeric>
#include <vector>

namespace adcc {
/**
 *  \defgroup Tensor Tensor interface
 */
///@{

/** The tensor interface used by adccore */
class Tensor {
 public:
  /** Construct a tensor interface class.
   *
   * adcmem_ptr     Memory keepalive object pointer
   */
  Tensor(std::shared_ptr<const AdcMemory> adcmem_ptr) : m_adcmem_ptr{adcmem_ptr} {}

  Tensor(Tensor&&) = default;
  Tensor& operator=(Tensor&&) = default;
  virtual ~Tensor()           = default;
  Tensor(const Tensor&)       = default;
  Tensor& operator=(const Tensor&) = default;

  //@{
  /** \name Interface of a tensor, which is exposed to python.
   */

  /** Number of dimensions */
  virtual size_t ndim() const = 0;

  /** Shape of each dimension */
  virtual std::vector<size_t> shape() const = 0;

  /** Number of elements */
  virtual size_t size() const = 0;

  // TODO It would be nice to have these two functions,
  //      but since this requires to store the mospaces or the symmetry
  //      object in this base class (instead of adcmem_ptr) or in the
  //      derived TensorImpl class. This is skipped for now, since
  //      in order to do this properly it requires to keep track of
  //      the spaces after all tensor operations (including contractions
  //      and the alike). At the moment this boils down to parsing
  //      the libtensor symmetry object to an adcc:Symmetry object
  //      from time to time. Just storing an MoSpaces pointer could
  //      already be a good start, is however not enough, since
  //      the "b" AoSpace is not covered by it ...
  //      Also in light of the fact, that we might want to replace
  //      libtensor at some point, it feels to me we are locking
  //      ourselves into their ecosystem to much with implementing this
  //      at the moment and beforeit is clear in which direction we will
  //      go in the future.
  //
  // /** Space to which the tensor is initialised */
  // virtual std::string space() const = 0;
  //
  // /** Return a Symmetry object representing the Symmetry of the tensor
  //  *  \note This represents a copy of the symmetry, i.e. the tensor
  //  *        cannot be modified using this function.
  //  */
  // virtual std::shared_ptr<Symmetry> symmetry_ptr() const = 0;

  /** Return a new tensor with the same dimensionality and symmetry
   *  as the passed tensor. The elements have undefined values. */
  virtual std::shared_ptr<Tensor> empty_like() const = 0;

  /** Return a new tensor with the same dimensionality and symmetry
   *  as the passed tensor and all elements set to zero. */
  virtual std::shared_ptr<Tensor> zeros_like() const = 0;

  /** Return a new tensor with the same dimensionality and symmetry
   *  as the passed tensor and all elements set to one. */
  virtual std::shared_ptr<Tensor> ones_like() const = 0;

  /** Return a new tensor with same dimensionality and shape
   *  (and bispace) but without any symmetry copied over */
  virtual std::shared_ptr<Tensor> nosym_like() const = 0;

  /** Return a deep copy of this tensor */
  virtual std::shared_ptr<Tensor> copy() const;

  /** Export a deep copy of this tensor to another tensor */
  virtual void copy_to(std::shared_ptr<Tensor> other) const = 0;

  /** Return a transposed form of this tensor as a *copy*
   *
   * \param axes  New permutation of the dimensions of this tensor (e.g.
   *              (1,0,2,3) will permute dimension 0 and 1 and keep the others)
   *              If missing, just reverse the dimension order.
   */
  virtual std::shared_ptr<Tensor> transpose(std::vector<size_t> axes) const = 0;

  /** Return the transposed form of a matrix as a *copy* */
  virtual std::shared_ptr<Tensor> transpose() const;

  /** Return the full trace of a tensor
   *
   * \param contraction Indices to contract over using einstein
   *                    summation convention, e.g. "abab" traces
   *                    over the 1st and 3rd and 2nd and 4th axis.
   */
  virtual double trace(std::string contraction) const = 0;
  virtual double trace() const { return trace("aa"); }

  /** In-place scale by a scalar value. */
  virtual void scale(scalar_type c) = 0;

  /** Set a mask into a tensor to a specific value.
   *  The mask to set is defined by the mask string. Repetitive
   *  indices define the values to be set. E.g. for a 6D tensor
   *  the mask string "iijkli" would set all elements T_{iijkli} for all
   *  ijkl to the given value.
   */
  virtual void set_mask(std::string mask, scalar_type value) = 0;

  /** Set the tensor to random data preserving symmetry */
  virtual void set_random() = 0;

  /** Compute the Frobenius or l2 inner product with a list of other tensors,
   *  returning the results as a scalar array */
  virtual std::vector<scalar_type> dot(
        std::vector<std::shared_ptr<Tensor>> tensors) const = 0;

  /** Compute the Frobenius or l2 inner product with another tensor */
  virtual scalar_type dot(std::shared_ptr<Tensor> other) const {
    return dot(std::vector<std::shared_ptr<Tensor>>{other})[0];
  }

  //@{
  /** Add a linear combination of tensors to this tensor
   *
   * scalars    List of scalar prefactors for the tensors
   * tensors    Tensors to add in
   */
  virtual void add(std::vector<scalar_type> scalars,
                   std::vector<std::shared_ptr<Tensor>> tensors) = 0;

  virtual void add(std::vector<std::shared_ptr<Tensor>> tensors) {
    const size_t size = tensors.size();
    add(std::vector<scalar_type>(size, 1.0), std::move(tensors));
  }

  virtual void add(const scalar_type c, std::shared_ptr<Tensor> other) {
    add(std::vector<scalar_type>{c}, {other});
  }

  virtual void add(std::shared_ptr<Tensor> other) { add(1.0, std::move(other)); }
  //@}

  /** Multiply another tensor to this tensor, that is form the expression
   *  out = this * other */
  virtual void multiply_to(std::shared_ptr<Tensor> other,
                           std::shared_ptr<Tensor> out) const = 0;

  /** Divide by another tensor, that is form the expression
   *  out = this / other */
  virtual void divide_to(std::shared_ptr<Tensor> other,
                         std::shared_ptr<Tensor> out) const = 0;

  // TODO Generalise this function by returning a type TensorOrScalar
  //      which either contains a tensor or a scalar. In this way
  //      full contractions, dot-products or traces can be handled
  //      by this method as well.

  /** Contract this tensor with another tensor and save the result in out.
   *  Let this tensor be A_{abcd} and we contract it with B_{cdef} over the
   *  indices c and d to form out_{abef}. This would be achieved using
   *  A.contract_to("abcd,cdef->abef", B, out)
   */
  virtual void contract_to(std::string contraction, std::shared_ptr<Tensor> other,
                           std::shared_ptr<Tensor> out) const = 0;

  /** Contract this tensor with another tensor and return the result.
   *  Let this tensor be A_{abcd} and we contract it with B_{cdef} over the
   *  indices c and d to form out_{abef}. This would be achieved using
   *  A.contract("abcd,cdef->abef", B)
   */
  virtual std::shared_ptr<Tensor> contract(std::string contraction,
                                           std::shared_ptr<Tensor> other) const = 0;

  /** Symmetrise with respect to the given index permutations
   *  by adding the elements resulting from appropriate index permutations.
   *
   * \param permutations    The list of permutations to be applied
   *                        *simultaneously*
   * \param out             The tensor to store the result in.
   *
   * Examples for permutations. Take a rank-4 tensor T_{ijkl}
   *    {{0,1}}             Permute the first two indices, i.e. form
   *                        0.5 * (T_{ijkl} + T_{jikl})
   *    {{0,1}, {2,3}}      Form 0.5 * (T_{ijkl} + T_{jilk})
   *
   * \note Unlike the implementation in libtensor, this function includes the
   *       prefactor 0.5
   */
  virtual void symmetrise_to(
        std::shared_ptr<Tensor> out,
        const std::vector<std::vector<size_t>>& permutations) const = 0;

  /** Antisymmetrise with respect to the given index permutations and export the
   *  result to the output tensor. For details with respect to the
   *  format of the permutations, see symmetrise_to. In this case the output tensor
   *  will be antisymmetric with respect to these permutations.
   *
   * \note Unlike the implementation in libtensor, this function includes the
   *       prefactor 0.5
   */
  virtual void antisymmetrise_to(
        std::shared_ptr<Tensor> out,
        const std::vector<std::vector<size_t>>& permutations) const = 0;

  /** Flag the tensor as immutable, allows some optimisations to be performed */
  virtual void set_immutable() = 0;

  /** Is the tensor mutable */
  virtual bool is_mutable() const = 0;

  /** Set the value of a single tensor element
   *  \note This is a slow function and should be avoided.
   **/
  virtual void set_element(const std::vector<size_t>& idx, scalar_type value) = 0;

  /** Get the value of a single tensor element
   *  \note This is a slow function and should be avoided.
   * */
  virtual scalar_type get_element(const std::vector<size_t>& tidx) const = 0;

  /** Return whether the element referenced by tidx is allowed (non-zero)
   *  by the symmetry of the Tensor or not.
   */
  virtual bool is_element_allowed(const std::vector<size_t>& tidx) const = 0;

  /** Get the n absolute largest elements along with their values
   *  \param n                     Number of elements to select
   *  \param unique_by_symmetry    By default the returned elements
   *                               are made unique by symmetry of the tensor.
   *                               Setting this to false disables this feature.
   **/
  virtual std::vector<std::pair<std::vector<size_t>, scalar_type>> select_n_absmax(
        size_t n, bool unique_by_symmetry = true) const = 0;

  /** Get the n absolute smallest elements along with their values
   *  \param n                     Number of elements to select
   *  \param unique_by_symmetry    By default the returned elements
   *                               are made unique by symmetry of the tensor.
   *                               Setting this to false disables this feature.
   **/
  virtual std::vector<std::pair<std::vector<size_t>, scalar_type>> select_n_absmin(
        size_t n, bool unique_by_symmetry = true) const = 0;

  /** Get the n largest elements along with their values
   *  \param n                     Number of elements to select
   *  \param unique_by_symmetry    By default the returned elements
   *                               are made unique by symmetry of the tensor.
   *                               Setting this to false disables this feature.
   **/
  virtual std::vector<std::pair<std::vector<size_t>, scalar_type>> select_n_max(
        size_t n, bool unique_by_symmetry = true) const = 0;

  /** Get the n smallest elements along with their values
   *  \param n                     Number of elements to select
   *  \param unique_by_symmetry    By default the returned elements
   *                               are made unique by symmetry of the tensor.
   *                               Setting this to false disables this feature.
   **/
  virtual std::vector<std::pair<std::vector<size_t>, scalar_type>> select_n_min(
        size_t n, bool unique_by_symmetry = true) const = 0;

  /** Print to an output stream */
  virtual void print(std::ostream& o) const = 0;

  /** Extract the tensor to plain memory provided by the given pointer.
   *
   *  \note This will return a full, *dense* tensor.
   *        At least size elements of space are assumed at the provided memory location.
   *        The data is stored in row-major (C-like) format
   */
  virtual void export_to(scalar_type* memptr, size_t size) const = 0;

  /** Extract the tensor into a std::vector, which will be resized to fit the data.
   * \note All data is stored in row-major (C-like) format
   */
  virtual void export_to(std::vector<scalar_type>& output) const {
    output.resize(size());
    export_to(output.data(), output.size());
  }

  /** Import the tensor from plain memory provided by the given
   *  pointer. The memory will be copied and all existing data overwritten.
   *  If symmetry_check is true, the process will check that the data has the
   *  required symmetry to fit into the tensor. This requires
   *  a slower algorithm to be chosen.
   *
   *  \param memptr      Full, dense memory pointer to the tensor data to be imported.
   *  \param size        Size of the dense memory.
   *  \param tolerance   Threshold to account for numerical inconsistencies
   *                     when checking the symmetry or for determining zero blocks.
   *  \param symmetry_check  Should symmetry be explicitly checked during the import.
   *
   *  \note This function requires a full, *dense* tensor with the data stored in
   *        row-major (C-like) format.
   */
  virtual void import_from(const scalar_type* memptr, size_t size,
                           scalar_type tolerance = 0, bool symmetry_check = true) = 0;

  /** Import the tensor from plain memory provided by the given
   *  vector. The memory will be copied and all existing data overwritten.
   *  If symmetry_check is true, the process will check that the data has the
   *  required symmetry to fit into the tensor. This requires
   *  a slower algorithm to be chosen.
   *
   *  \param input       Input data in a linearised vector
   *  \param tolerance   Threshold to account for numerical inconsistencies
   *                     when checking the symmetry or for determining zero blocks.
   *  \param symmetry_check  Should symmetry be explicitly checked during the import.
   *
   *  \note This function requires a full, *dense* tensor with the data stored in
   *        row-major (C-like) format.
   */
  virtual void import_from(const std::vector<scalar_type>& input,
                           scalar_type tolerance = 0, bool symmetry_check = true) {
    import_from(input.data(), input.size(), tolerance, symmetry_check);
  }

  /** Import the tensor from a generator functor. All existing data will be overwritten.
   *  If symmetry_check is true, the process will check that the data has the
   *  required symmetry to fit into the tensor. This requires
   *  a slower algorithm to be chosen.
   *
   *  \param generator   Generator functor. The functor is called with a list of ranges
   *                     for each dimension. The ranges are half-open, left-inclusive
   *                     and right-exclusive. The corresponding data should be written
   *                     to the passed pointer into raw memory. This is an advanced
   *                     functionality. Use only if you know what you are doing.
   *  \param tolerance   Threshold to account for numerical inconsistencies
   *                     when checking the symmetry or for determining zero blocks.
   *  \param symmetry_check  Should symmetry be explicitly checked during the import.
   *
   *  \note The generator is required to produce data in row-major (C-like) format
   *        at a designated memory location.
   */
  virtual void import_from(
        std::function<void(const std::vector<std::pair<size_t, size_t>>&, scalar_type*)>
              generator,
        scalar_type tolerance = 0, bool symmetry_check = true) = 0;

  /**
   * Return a std::string providing hopefully helpful information
   * about the symmetries stored inside the tensor object.
   */
  virtual std::string describe_symmetry() const = 0;
  //@}

  /** Return a pointer to the memory keep-alive object */
  std::shared_ptr<const AdcMemory> adcmem_ptr() const { return m_adcmem_ptr; }

 protected:
  // Pointer to the adc memory object to keep memory alive.
  std::shared_ptr<const AdcMemory> m_adcmem_ptr;
};

//
// Some operators
//

/** Write a string representation of the Tensor to the provided stream */
inline std::ostream& operator<<(std::ostream& out, const Tensor& tensor) {
  tensor.print(out);
  return out;
}

/** Contract tensor A with another tensor and return the result.
 *  Let this tensor be A_{abcd} and we contract it with B_{cdef} over the
 *  indices c and d to form out_{abef}. This would be achieved using
 *  A.contract("abcd,cdef->abef", B)
 */
inline std::shared_ptr<Tensor> contract(std::string contraction,
                                        std::shared_ptr<Tensor> A,
                                        std::shared_ptr<Tensor> B) {
  return A->contract(contraction, B);
}

/** Construct a tensor initialised to zero using a Symmetry object */
std::shared_ptr<Tensor> make_tensor_zero(std::shared_ptr<Symmetry> symmetry);
// Note: Unlike most other functions in this header, this function
//       is only implemented in the file TensorImpl.cc

/** Construct an empty (uninitialised) tensor using a Symmetry object */
std::shared_ptr<Tensor> make_tensor_empty(std::shared_ptr<Symmetry> symmetry);
// Note: Unlike most other functions in this header, this function
//       is only implemented in the file TensorImpl.cc

///@}
}  // namespace adcc
