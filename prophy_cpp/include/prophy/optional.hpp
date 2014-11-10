// Copyright (C) 2003, 2008 Fernando Luis Cacciola Carballal.
//
// Use, modification, and distribution is subject to the Boost Software
// License, Version 1.0. (See accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
//
// See http://www.boost.org/libs/optional for documentation.
//
// You are welcome to contact the author at:
//  fernando_cacciola@hotmail.com
//
// Revisions:
// 27 Apr 2008 (improved swap) Fernando Cacciola, Niels Dekker, Thorsten Ottosen
//

#ifndef _PROPHY_OPTIONAL_HPP
#define _PROPHY_OPTIONAL_HPP

#include <stdint.h>
#include <cstddef>
#include <cassert>

namespace prophy
{

template<class T>
class optional;

namespace optional_detail
{

template <std::size_t N>
struct type_with_alignment
{
   // We should never get to here, but if we do use the maximally
   // aligned type:
   // BOOST_STATIC_ASSERT(0);
   typedef uint64_t type;
};
template <> struct type_with_alignment<1>{ typedef uint8_t type; };
template <> struct type_with_alignment<2>{ typedef uint16_t type; };
template <> struct type_with_alignment<4>{ typedef uint32_t type; };
template <> struct type_with_alignment<8>{ typedef uint64_t type; };

template <typename T>
struct alignment_of
{
    struct finder
    {
        char align;
        T t;
    };
    enum { value = sizeof(finder) - sizeof(T) };
};

// This local class is used instead of that in "aligned_storage.hpp"
// because I've found the 'official' class to ICE BCB5.5
// when some types are used with optional<>
// (due to sizeof() passed down as a non-type template parameter)
template <class T>
class aligned_storage
{
    // Borland ICEs if unnamed unions are used for this!
    union dummy_u
    {
        char data[ sizeof(T) ];
        typename type_with_alignment<alignment_of<T>::value >::type aligner_;
    } dummy_ ;

public:

    void const* address() const { return dummy_.data; }
    void      * address()       { return dummy_.data; }
};

template<class T>
struct types_when_isnt_ref
{
  typedef T const& reference_const_type ;
  typedef T &      reference_type ;
  typedef T const* pointer_const_type ;
  typedef T *      pointer_type ;
  typedef T const& argument_type ;
};

template<class T>
class optional_base
{
private:

    typedef T internal_type;

    typedef aligned_storage<internal_type> storage_type;

    typedef types_when_isnt_ref<T> types_when_not_ref;

    typedef optional_base<T> this_type;

protected:

    typedef T value_type;

public:
    typedef types_when_not_ref types;

protected:
    typedef bool (this_type::*unspecified_bool_type)() const;

    typedef typename types::reference_type       reference_type;
    typedef typename types::reference_const_type reference_const_type;
    typedef typename types::pointer_type         pointer_type;
    typedef typename types::pointer_const_type   pointer_const_type;
    typedef typename types::argument_type        argument_type;

    // Creates an optional<T> uninitialized.
    // No-throw
    optional_base()
      :
      m_initialized(false) {}

    // Creates an optional<T> initialized with 'val'.
    // Can throw if T::T(T const&) does
    optional_base ( argument_type val )
      :
      m_initialized(false)
    {
      construct(val);
    }

    // Creates an optional<T> initialized with 'val' IFF cond is true, otherwise creates an uninitialzed optional<T>.
    // Can throw if T::T(T const&) does
    optional_base ( bool cond, argument_type val )
      :
      m_initialized(false)
    {
      if ( cond )
        construct(val);
    }

    // Creates a deep copy of another optional<T>
    // Can throw if T::T(T const&) does
    optional_base ( optional_base const& rhs )
      :
      m_initialized(false)
    {
      if ( rhs.is_initialized() )
        construct(rhs.get_impl());
    }

    // No-throw (assuming T::~T() doesn't)
    ~optional_base() { destroy(); }

    // Assigns from another optional<T> (deep-copies the rhs value)
    void assign ( optional_base const& rhs )
    {
      if (is_initialized())
      {
        if ( rhs.is_initialized() )
             assign_value(rhs.get_impl());
        else destroy();
      }
      else
      {
        if ( rhs.is_initialized() )
          construct(rhs.get_impl());
      }
    }

    // Assigns from another _convertible_ optional<U> (deep-copies the rhs value)
    template<class U>
    void assign ( optional<U> const& rhs )
    {
      if (is_initialized())
      {
        if ( rhs.is_initialized() )
             assign_value(static_cast<value_type>(rhs.get()));
        else destroy();
      }
      else
      {
        if ( rhs.is_initialized() )
          construct(static_cast<value_type>(rhs.get()));
      }
    }

    // Assigns from a T (deep-copies the rhs value)
    void assign ( argument_type val )
    {
      if (is_initialized())
           assign_value(val);
      else construct(val);
    }

  public :

    // Destroys the current value, if any, leaving this UNINITIALIZED
    // No-throw (assuming T::~T() doesn't)
    void reset() { destroy(); }

    // Replaces the current value -if any- with 'val'
    void reset ( argument_type val ) { assign(val); }

    // Returns a pointer to the value if this is initialized, otherwise,
    // returns NULL.
    // No-throw
    pointer_const_type get_ptr() const { return m_initialized ? get_ptr_impl() : 0; }
    pointer_type       get_ptr()       { return m_initialized ? get_ptr_impl() : 0; }

    bool is_initialized() const { return m_initialized; }

  protected :

    void construct ( argument_type val )
     {
       new (m_storage.address()) internal_type(val);
       m_initialized = true;
     }

    void assign_value ( argument_type val ) { get_impl() = val; }

    void destroy()
    {
      if ( m_initialized )
        destroy_impl();
    }

    unspecified_bool_type safe_bool() const { return m_initialized ? &this_type::is_initialized : 0; }

    reference_const_type get_impl() const { return dereference(get_object()); }
    reference_type       get_impl()       { return dereference(get_object()); }

    pointer_const_type get_ptr_impl() const { return cast_ptr(get_object()); }
    pointer_type       get_ptr_impl()       { return cast_ptr(get_object()); }

  private :

    internal_type const* get_object() const { return static_cast<internal_type const*>(m_storage.address()); }
    internal_type *      get_object()       { return static_cast<internal_type *>     (m_storage.address()); }

    // reference_content<T> lacks an implicit conversion to T&, so the following is needed to obtain a proper reference.
    reference_const_type dereference( internal_type const* p ) const { return *p; }
    reference_type       dereference( internal_type*       p )       { return *p; }

    void destroy_impl ( ) { get_ptr_impl()->~T(); m_initialized = false; }

    // If T is of reference type, trying to get a pointer to the held value must result in a compile-time error.
    // Decent compilers should disallow conversions from reference_content<T>* to T*, but just in case,
    // the following olverloads are used to filter out the case and guarantee an error in case of T being a reference.
    pointer_const_type cast_ptr( internal_type const* p ) const { return p; }
    pointer_type       cast_ptr( internal_type *      p )       { return p; }

    bool m_initialized;
    storage_type m_storage;
};

} // namespace optional_detail

template<class T>
class optional : public optional_detail::optional_base<T>
{
    typedef optional_detail::optional_base<T> base;

    typedef typename base::unspecified_bool_type unspecified_bool_type;

public:

    typedef optional<T> this_type;

    typedef typename base::value_type           value_type;
    typedef typename base::reference_type       reference_type;
    typedef typename base::reference_const_type reference_const_type;
    typedef typename base::pointer_type         pointer_type;
    typedef typename base::pointer_const_type   pointer_const_type;
    typedef typename base::argument_type        argument_type;

    // Creates an optional<T> uninitialized.
    // No-throw
    optional() : base() {}

    // Creates an optional<T> initialized with 'val'.
    // Can throw if T::T(T const&) does
    optional ( argument_type val ) : base(val) {}

    // Creates an optional<T> initialized with 'val' IFF cond is true, otherwise creates an uninitialized optional.
    // Can throw if T::T(T const&) does
    optional ( bool cond, argument_type val ) : base(cond,val) {}

    // NOTE: MSVC needs templated versions first

    // Creates a deep copy of another convertible optional<U>
    // Requires a valid conversion from U to T.
    // Can throw if T::T(U const&) does
    template<class U>
    explicit optional ( optional<U> const& rhs )
      :
      base()
    {
      if ( rhs.is_initialized() )
        this->construct(rhs.get());
    }

    // Creates a deep copy of another optional<T>
    // Can throw if T::T(T const&) does
    optional ( optional const& rhs ) : base( static_cast<base const&>(rhs) ) {}

   // No-throw (assuming T::~T() doesn't)
    ~optional() {}

    // Assigns from another convertible optional<U> (converts && deep-copies the rhs value)
    // Requires a valid conversion from U to T.
    // Basic Guarantee: If T::T( U const& ) throws, this is left UNINITIALIZED
    template<class U>
    optional& operator= ( optional<U> const& rhs )
      {
        this->assign(rhs);
        return *this;
      }

    // Assigns from another optional<T> (deep-copies the rhs value)
    // Basic Guarantee: If T::T( T const& ) throws, this is left UNINITIALIZED
    //  (NOTE: On BCB, this operator is not actually called and left is left UNMODIFIED in case of a throw)
    optional& operator= ( optional const& rhs )
      {
        this->assign( static_cast<base const&>(rhs) );
        return *this;
      }

    // Assigns from a T (deep-copies the rhs value)
    // Basic Guarantee: If T::( T const& ) throws, this is left UNINITIALIZED
    optional& operator= ( argument_type val )
      {
        this->assign( val );
        return *this;
      }

    void swap( optional & arg )
      {
        // allow for Koenig lookup
        swap(*this, arg);
      }

    // Returns a reference to the value if this is initialized, otherwise,
    // the behaviour is UNDEFINED
    // No-throw
    reference_const_type get() const { assert(this->is_initialized()); return this->get_impl(); }
    reference_type       get()       { assert(this->is_initialized()); return this->get_impl(); }

    // Returns a copy of the value if this is initialized, 'v' otherwise
    reference_const_type get_value_or ( reference_const_type v ) const { return this->is_initialized() ? get() : v; }
    reference_type       get_value_or ( reference_type       v )       { return this->is_initialized() ? get() : v; }

    // Returns a pointer to the value if this is initialized, otherwise,
    // the behaviour is UNDEFINED
    // No-throw
    pointer_const_type operator->() const { assert(this->is_initialized()); return this->get_ptr_impl(); }
    pointer_type       operator->()       { assert(this->is_initialized()); return this->get_ptr_impl(); }

    // Returns a reference to the value if this is initialized, otherwise,
    // the behaviour is UNDEFINED
    // No-throw
    reference_const_type operator *() const { return this->get(); }
    reference_type       operator *()       { return this->get(); }

    // implicit conversion to "bool"
    // No-throw
    operator unspecified_bool_type() const { return this->safe_bool(); }

    // This is provided for those compilers which don't like the conversion to bool
    // on some contexts.
    bool operator!() const { return !this->is_initialized(); }
};

} // namespace prophy

#endif  /* _PROPHY_OPTIONAL_HPP */
