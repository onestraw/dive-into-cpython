/* ------- ------ ------ object.h ------ ------ ------ ------ ----- */

/* PyObject_HEAD defines the initial segment of every PyObject. */
#define PyObject_HEAD                   \
    _PyObject_HEAD_EXTRA                \
    Py_ssize_t ob_refcnt;               \
    struct _typeobject *ob_type;

/* PyObject_VAR_HEAD defines the initial segment of all variable-size
 * container objects.  These end with a declaration of an array with 1
 * element, but enough space is malloc'ed so that the array actually
 * has room for ob_size elements.  Note that ob_size is an element count,
 * not necessarily a byte count.
 */
#define PyObject_VAR_HEAD               \
    PyObject_HEAD                       \
    Py_ssize_t ob_size; /* Number of items in variable part */
#define Py_INVALID_SIZE (Py_ssize_t)-1

/* Nothing is actually declared to be a PyObject, but every pointer to
 * a Python object can be cast to a PyObject*.  This is inheritance built
 * by hand.  Similarly every pointer to a variable-size Python object can,
 * in addition, be cast to PyVarObject*.
 */
typedef struct _object {
    PyObject_HEAD
} PyObject;

typedef struct {
    PyObject_VAR_HEAD
} PyVarObject;


#define Py_REFCNT(ob)           (((PyObject*)(ob))->ob_refcnt)
#define Py_TYPE(ob)             (((PyObject*)(ob))->ob_type)
#define Py_SIZE(ob)             (((PyVarObject*)(ob))->ob_size)


/* ------- ------ ------ intobject.h ------ ------ ------ ------ ----- */
typedef struct {
    PyObject_HEAD
    long ob_ival;
} PyIntObject;


/* ------- ------ ------ stringobject.h ------ ------ ------ ----- */
typedef struct {
    PyObject_VAR_HEAD
    long ob_shash;
    int ob_sstate;
    char ob_sval[1];

    /* Invariants:
     *     ob_sval contains space for 'ob_size+1' elements.
     *     ob_sval[ob_size] == 0.
     *     ob_shash is the hash of the string or -1 if not computed yet.
     *     ob_sstate != 0 iff the string object is in stringobject.c's
     *       'interned' dictionary; in this case the two references
     *       from 'interned' to this object are *not counted* in ob_refcnt.
     */
} PyStringObject;

/* ------- ------ ------ listobject.h ------ ------ ------ ----- */
typedef struct {
    PyObject_VAR_HEAD
    /* Vector of pointers to list elements.  list[0] is ob_item[0], etc. */
    PyObject **ob_item;

    /* ob_item contains space for 'allocated' elements.  The number
     * currently in use is ob_size.
     * Invariants:
     *     0 <= ob_size <= allocated
     *     len(list) == ob_size
     *     ob_item == NULL implies ob_size == allocated == 0
     * list.sort() temporarily sets allocated to -1 to detect mutations.
     *
     * Items must normally not be NULL, except during construction when
     * the list is not yet visible outside the function that builds it.
     */
    Py_ssize_t allocated;
} PyListObject;

/* ------- ------ ------ ceval.c ------ ------ ------ ----- */
PyObject *
PyEval_EvalFrameEx(PyFrameObject *f, int throwflag)
{
        TARGET_NOARG(BINARY_ADD)
        {
            w = POP();
            v = TOP();
            if (PyInt_CheckExact(v) && PyInt_CheckExact(w)) {
                /* INLINE: int + int */
                register long a, b, i;
                a = PyInt_AS_LONG(v);
                b = PyInt_AS_LONG(w);
                /* cast to avoid undefined behaviour
                   on overflow */
                i = (long)((unsigned long)a + b);
                if ((i^a) < 0 && (i^b) < 0)
                    goto slow_add;
                x = PyInt_FromLong(i);
            }
            else if (PyString_CheckExact(v) &&
                     PyString_CheckExact(w)) {
                x = string_concatenate(v, w, f, next_instr);
                /* string_concatenate consumed the ref to v */
                goto skip_decref_vx;
            }
            else {
              slow_add:
                x = PyNumber_Add(v, w);
            }
            Py_DECREF(v);
          skip_decref_vx:
            Py_DECREF(w);
            SET_TOP(x);
            if (x != NULL) DISPATCH();
            break;
        }

}


#define PyInt_CheckExact(op) (Py_TYPE(op) == &PyInt_Type)
#define PyString_CheckExact(op) (Py_TYPE(op) == &PyString_Type)
