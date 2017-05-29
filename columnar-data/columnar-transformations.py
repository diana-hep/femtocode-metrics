from functools import reduce
import math
import sys
import re

import numpy

# Schema inference (if not given, e.g. dynamically typed languages)
# 
# Rules:
#   * integer (whole numbers) is a subtype of number (any machine-representable numbers)
#   * boolean, integer/number, string are concrete types, represented as singleton sets:
#       {"boolean"}
#       {"integer"}
#       {"number"}
#       {"string"}
#   * sequence is parameterized by one type, represented as singleton dicts:
#       {"sequence": PARAM}
#   * record is parameterized by a non-negative number of fields, represented as singleton dicts of a name-type dict:
#       {"record": {"NAME1": PARAM1, "NAME2": PARAM2, ...}}
#   * {"unknown"} is a placeholder, used during schema inference
#   * the schema of an empty sequence is {"sequence": {"unknown"}}
#   * schema inference proceeds via a depth-first walk over the data,
#       first inferring from leaves upward
#       then resolving unknowns from sequences and records downward
#   * the following types are disjoint and are incompatible in a sequence (sequences are homogeneous):
#       boolean
#       number (integer expands to number if any item is not integral)
#       string
#       sequences parameterized by different types, expanding integers to numbers if necessary (sequences are covariant in this subtype relationship)
#       records with fields of the same name and different types (missing names are allowed)
#   * the following are all considered missing (and therefore equivalent):
#       None
#       float value NaN
#       int with the same bit pattern as NaN (intnan, which is near the end of the int range)
#       record lacking the desired field
#
# Note that this type system does not permit:
#   * recursive types (e.g. arbitrary-depth trees)
#   * pointers or cross-references
#   * disjoint union types or class inheritance (which is a special case)

floatnan = float("nan")
intnan = numpy.asscalar(numpy.cast["int64"](numpy.float64("nan")))

def generic(sch):
    """
    Extract the generic name from a schema (set or dict).
    """
    for x in sch:
        return x

def param(sch):
    """
    Extract the parameterization of a schema (dict only).
    """
    if sch == {"unknown"}:
        return {"unknown"}
    for x in sch.values():
        return x

def consistent(schs):
    """
    Determine if a set of schemas are consistent with one another and can therefore be members of the same homogeneous sequence.

    This method descends toward the leaves to resolve unknowns.

    Parameters
      schs: a list (not generator) of schemas

    Returns
      the common type of all of the schemas, expanding integer to number if necessary

    Raises
      TypeError if schemas are not consistent
    """
    if len(schs) == 0 or all(x == {"unknown"} for x in schs):
        return {"unknown"}
    elif all(x == {"unknown"} or x == {"boolean"} for x in schs):
        return {"boolean"}
    elif all(x == {"unknown"} or x == {"integer"} for x in schs):
        return {"integer"}
    elif all(x == {"unknown"} or x == {"integer"} or x == {"number"} for x in schs):
        return {"number"}
    elif all(x == {"unknown"} or x == {"string"} for x in schs):
        return {"string"}
    elif all(x == {"unknown"} or generic(x) == "sequence" for x in schs):
        return {"sequence": consistent([param(x) for x in schs])}
    elif all(x == {"unknown"} or generic(x) == "record" for x in schs):
        fieldnames = reduce(lambda x, y: x.union(y), (set(param(x)) for x in schs if x != {"unknown"}), set())
        return {"record": {n: consistent([param(x).get(n, {"unknown"}) for x in schs if param(x) != {"unknown"}]) for n in fieldnames}}
    else:
        raise TypeError("schs are not consistent: {}".format(", ".join(map(str, schs))))

def schema(obj):
    """
    Determine the schema of the given object.

    This method ascends from leaves to root and calls consistent to descend back toward the leaves to resolve unknowns.

    Parameters
      obj: Python object made of numbers, booleans, lists, and dicts

    Returns
      a schema specification, which is either a singleton set or a singleton dict

    Raises
      TypeError for unrecognize Python types
    """
    if obj is None or (isinstance(obj, float) and math.isnan(obj)) or obj == intnan:
        return {"unknown"}
    elif isinstance(obj, bool):
        return {"boolean"}
    elif isinstance(obj, int):
        return {"integer"}
    elif isinstance(obj, float):
        return {"number"}
    elif isinstance(obj, str):
        return {"string"}
    elif isinstance(obj, list):
        return {"sequence": consistent([schema(x) for x in obj])}
    elif isinstance(obj, dict):
        return {"record": {n: schema(v) for n, v in obj.items()}}
    else:
        raise TypeError("unrecognized type: {}".format(type(obj)))

def satisfies(obj, sch):
    """
    Determine if the object satisfies the schema.

    This is provided as a cross-check; it would return True for any schema generated from the object by the schema function.

    Parameters
      obj: Python object made of numbers, booleans, lists, and dicts
      sch: a schema specification, which is either a singleton set or a singleton dict

    Returns
      True if obj satisfies sch, False otherwise
    """

    if obj is None:
        return True
    elif isinstance(obj, bool) and sch == {"boolean"}:
        return True
    elif isinstance(obj, (int, float)) and sch == {"number"}:
        return True
    elif isinstance(obj, int) and sch == {"integer"}:
        return True
    elif isinstance(obj, str) and sch == {"string"}:
        return True
    elif isinstance(obj, list):
        if len(obj) == 0:
            return generic(sch) == "sequence"
        else:
            return all(satisfies(x, param(sch)) for x in obj)
    elif isinstance(obj, dict):
        if any(n not in param(sch) for n in obj):
            return False
        return all(satisfies(v, param(sch)[n]) for n, v in obj.items())
    else:
        return False

########################## isolate Python 2/3 differences in encoding

# for a byte array type (as opposed to Unicode strings), don't encode/decode

def encode(string):
    """
    Turn a Unicode string into a list of byte values (Python 2) or a bytes object (Python 3).

    Normalizes behavior between Python versions.
    """
    if sys.version_info[0] <= 2:
        if isinstance(string, unicode):
            return map(ord, string.encode("utf8"))
        else:
            return map(ord, string)
    else:
        if isinstance(string, str):
            return string.encode("utf8")
        else:
            return string

def decode(values):
    """
    Turn a list of byte values into a Unicode string.

    Normalizes behavior between Python versions.
    """
    if sys.version_info[0] <= 2:    
        return "".join(map(chr, values)).decode("utf8")
    else:
        return bytes(values).decode("utf8")

########################## recursive counter (extension of ROOT)

def newarrays(sch, name):
    """
    Create empty lists that will be filled as arrays by the toflat function.

    Array sizes are not predicted (hence the Python lists and 'append' in toflat).

    Parameters
      sch: a schema specification, which is either a singleton set or a singleton dict
      name: base name for all arrays produced

    Returns
      a dict of empty Python lists with appropriate names
    """
    def recurse(sch, name, sizename):  # hide the sizename with a nested recursive function
        if sch == {"boolean"} or sch == {"integer"} or sch == {"number"}:
            if sizename is None:
                return {name: []}
            else:
                return {name: [], sizename + "@size": []}

        elif sch == {"string"}:
            name = name + "$"                              # the '$' marks it as a string
            return {name: [], name + "@size": []}

        elif generic(sch) == "sequence":
            name = name + "[]"                             # the '[]' marks it as a sequence
            return recurse(param(sch), name, name)

        elif generic(sch) == "record":
            out = {}
            for n, s in param(sch).items():                # record paths are delimited by '-'
                out.update(recurse(s, name + "-" + n, sizename))
            return out

        else:
            assert False, "schema is {}".format(sch)

    return recurse(sch, name, None)    # sizename starts as None

def toflat(obj, sch, arrays, name):
    """
    Fill arrays with a flattened version of the given object.

    This is the opposite of fromflat.

    Parameters
      obj: Python object made of numbers, booleans, lists, and dicts
      sch: a schema specification, which is either a singleton set or a singleton dict
      arrays: dict of empty Python lists with appropriate names
      name: the base name to find in arrays

    Returns
      nothing; called to modify arrays in place
    """
    assert satisfies(obj, sch)

    if sch == {"boolean"}:
        if obj is False:
            arrays[name].append(0)
        elif obj is True:
            arrays[name].append(1)
        elif obj is None:
            arrays[name].append(2)

    elif sch == {"integer"}:
        if obj is None:
            arrays[name].append(intnan)
        else:
            arrays[name].append(int(obj))

    elif sch == {"number"}:
        if obj is None:
            arrays[name].append(floatnan)
        else:
            arrays[name].append(float(obj))

    elif sch == {"string"}:
        if obj is None:
            arrays[name + "$@size"].append(-1)
        else:
            encoded = encode(obj)
            arrays[name + "$"].extend(encoded)
            arrays[name + "$@size"].append(len(encoded))

    elif generic(sch) == "sequence":
        if obj is None:
            length = -1
        else:
            length = len(obj)

        for n, a in arrays.items():
            if n.endswith("@size") and n.startswith(name):
                a.append(length)

        if obj is not None:
            for x in obj:
                toflat(x, param(sch), arrays, name + "[]")

    elif generic(sch) == "record":
        for n, s in param(sch).items():
            if obj is None or n not in obj:
                toflat(None, s, arrays, name + "-" + n)
            else:
                toflat(obj[n], s, arrays, name + "-" + n)

    else:
        assert False, "schema is {}".format(sch)

def tonumpy(arrays, **schemas):
    """
    Convert flat Python lists into flat Numpy arrays.

    The original lists are not overwritten.

    Parameters
      arrays: dict of filled Python lists with appropriate names
      **schemas: base names to schemas that we should look for in arrays

    Returns
      dict of Numpy arrays corresponding to the base names provided as keyword arguments
    """
    out = {}

    def recurse(sch, name, sizename):
        if sch == {"boolean"}:
            out[name] = numpy.array(arrays[name], dtype=numpy.uint8)
            if sizename is not None:
                sizename = sizename + "@size"
                out[sizename] = numpy.array(arrays[sizename], dtype=numpy.int64)

        elif sch == {"integer"}:
            out[name] = numpy.array(arrays[name], dtype=numpy.int64)
            if sizename is not None:
                sizename = sizename + "@size"
                out[sizename] = numpy.array(arrays[sizename], dtype=numpy.int64)

        elif sch == {"number"}:
            out[name] = numpy.array(arrays[name], dtype=numpy.float64)
            if sizename is not None:
                sizename = sizename + "@size"
                out[sizename] = numpy.array(arrays[sizename], dtype=numpy.int64)

        elif sch == {"string"}:
            name = name + "$"
            sizename = name + "@size"
            out[name] = numpy.array(arrays[name], dtype=numpy.uint8)
            out[sizename] = numpy.array(arrays[sizename], dtype=numpy.int64)

        elif generic(sch) == "sequence":
            name = name + "[]"
            recurse(param(sch), name, name)

        elif generic(sch) == "record":
            for n, s in param(sch).items():
                recurse(s, name + "-" + n, sizename)

        else:
            assert False, "schema is {}".format(sch)

    for name, sch in schemas.items():
        recurse(sch, name, None)

    return out

def savenpz(file, arrays, **schemas):
    """
    Save arrays to a Numpy .npz file.

    Parameters
      file: file handle open for writing binary (or a file name string)
      arrays: dict of filled Python lists with appropriate names
      **schemas: base names to schemas that we should look for in arrays

    Returns
      nothing; called to write or overwrite file
    """
    if isinstance(file, str):
        file = open(str, "wb")
    numpy.savez_compressed(file, tonumpy(arrays, **schemas))

def loadnpz(file, name):
    """
    Load arrays from a Numpy .npz file.

    Parameters
      file: file handle open for reading binary (or a file name string)
      name: base name of interest

    Returns
      Numpy arrays corresponding to a flattened Numpy object
    """
    if isinstance(file, str):
        file = open(str, "rb")
    handle = numpy.load(file)
    arrays = {}
    for n in handle.keys():
        if n.startswith(name):
            arrays[n] = handle[n]
    return arrays

def getschema(arrays, name):
    """
    Deduce the schema from array names with a given base.

    The naming convention encodes structure and Numpy array dtypes distinguish primitive types. This way, a schema object does not need to be separately stored in the file.

    Parameters
      arrays: dict of filled Numpy arrays (must be Numpy, not Python lists)
      name: base name of interest

    Returns
      a schema specification, which is either a singleton set or a singleton dict
    """
    if name + "$" in arrays:
        return {"string"}

    elif name in arrays:
        if arrays[name].dtype == numpy.uint8:
            return {"boolean"}
        elif arrays[name].dtype == numpy.int64:
            return {"integer"}
        elif arrays[name].dtype == numpy.float64:
            return {"number"}
        else:
            assert False, "{} has dtype {}".format(name, arrays[name].dtype)

    elif any(not n.endswith("@size") and n.startswith(name + "[]") for n in arrays):
        trimmed = {name + n[len(name) + 2:]: v for n, v in arrays.items() if n.startswith(name + "[]") and n != name + "[]@size"}
        return {"sequence": getschema(trimmed, name)}

    else:
        trimmed = {n[len(name) + 1:]: v for n, v in arrays.items() if n.startswith(name + "-")}
        fields = {}
        for n in trimmed:
            if not n.endswith("@size"):
                fn = re.match(r"([^-@[$]*)", n).group(1)
                fields[fn] = getschema(trimmed, fn)
        return {"record": fields}

def fromflat(arrays, sch, name):
    """
    Reconstruct a Python object from flattened arrays.

    This is the opposite of toflat.

    Parameters
      arrays: dict of filled Python lists or Numpy arrays
      sch: a schema specification, which is either a singleton set or a singleton dict
      name: base name of interest

    Returns
      Python object made of numbers, booleans, lists, and dicts
    """
    def recurse(arrays, sch, name, indexes):
        if sch == {"boolean"}:
            value = arrays[name][indexes[name]]
            indexes[name] += 1

            if value == 0:
                return False
            elif value == 1:
                return True
            elif value == 2:
                return None
            else:
                assert False

        elif sch == {"integer"}:
            value = arrays[name][indexes[name]]
            indexes[name] += 1

            if value == intnan:
                return None
            else:
                return int(value)

        elif sch == {"number"}:
            value = arrays[name][indexes[name]]
            indexes[name] += 1

            if math.isnan(value):
                return None
            else:
                return float(value)

        elif sch == {"string"}:
            sizename = name + "$@size"
            length = arrays[sizename][indexes[sizename]]
            indexes[sizename] += 1

            if length == -1:
                return None
            else:
                name = name + "$"
                values = arrays[name][indexes[name] : indexes[name] + length]
                indexes[name] += length
                return decode(values)

        elif generic(sch) == "sequence":
            length = None
            for n, a in arrays.items():
                if n.endswith("@size") and n.startswith(name):
                    l = arrays[n][indexes[n]]
                    indexes[n] += 1
                    if length is None:
                        length = l
                    else:
                        assert l == length, "misaligned sequence index"

            assert length is not None, "missing sequence index"

            if length == -1:
                return None
            else:
                return [recurse(arrays, param(sch), name + "[]", indexes) for i in range(length)]

        elif generic(sch) == "record":
            return {n: recurse(arrays, s, name + "-" + n, indexes) for n, s in param(sch).items()}

        else:
            assert False, "schema is {}".format(sch)

    return recurse(arrays, sch, name, {n: 0 for n in arrays})

########################## repetition and definition levels (Parquet)

def newarrays(sch, name):
    # generate all projections separately and later coalesce them in tonumpy
    if sch == {"boolean"} or sch == {"integer"} or sch == {"number"}:
        return {name: [], name + "@def": [], name + "@rep": []}

    elif sch == {"string"}:
        name = name + "$"
        return {name: [], name + "@def": [], name + "@rep": []}

    elif generic(sch) == "sequence":
        return newarrays(param(sch), name + "[]")

    elif generic(sch) == "record":
        out = {}
        for n, s in param(sch).items():
            out.update(newarrays(s, name + "-" + n))
        return out

    else:
        assert False, "schema is {}".format(sch)

def toflat(obj, sch, arrays, name):
    # separate pass over the data for each projection; not efficient, but illustrative
    for projection in arrays:
        if projection.startswith(name) and not projection.endswith("@def") and not projection.endswith("@rep"):
            dataarray = arrays[projection]
            defarray = arrays[projection + "@def"]
            reparray = arrays[projection + "@rep"]

            def undefined(sch, deflevel, first, replevel, rep):
                if not first:
                    replevel = rep

                if sch == {"number"}:
                    defarray.append(deflevel)
                    reparray.append(replevel)

                elif generic(sch) == "sequence":
                    undefined(param(sch), deflevel, first, replevel, rep)

            def defined(obj, sch, deflevel, first, replevel, rep):
                if not first:
                    replevel = rep

                if sch == {"number"}:
                    dataarray.append(obj)
                    defarray.append(deflevel)
                    reparray.append(replevel)

                elif generic(sch) == "sequence":
                    if len(obj) == 0:
                        undefined(param(sch), deflevel, True, replevel, None)
                    else:
                        first = True
                        for x in obj:
                            if x is None:
                                undefined(param(sch), deflevel, first, replevel, rep + 1)
                            else:
                                defined(x, param(sch), deflevel + 1, first, replevel, rep + 1)
                            first = False

            if obj is None:
                undefined(sch, 0, 0)
            else:
                defined(obj, sch, 0, False, 0, 0)

obj = [[[1.1, 2.2, 3.3], None], [[99.9], [3.14, 2.71]]]
print(obj)
name = "x"
sch = schema(obj)
print(sch)
arrays = newarrays(sch, name)
toflat(obj, sch, arrays, name)
for key in sorted(arrays):
    print(key, arrays[key])

import sys
sys.exit(0)

########################## tests

import random

def roundtrip(obj, flattened, expectation, debug=False):
    name = "x"
    sch = schema(obj)
    if debug:
        print(sch)
        print("")
    arrays = newarrays(sch, name)
    toflat(obj, sch, arrays, name)
    if debug:
        print(arrays)
        print(flattened)
        print("")
    assert arrays == flattened
    result = fromflat(arrays, sch, name)
    if debug:
        print(result)
        print(expectation)
        print("")
    assert result == expectation

def schema2name(obj, debug=False):
    name = "x"
    sch = schema(obj)
    if debug:
        print(sch)
    arrays = newarrays(sch, name)
    toflat(obj, sch, arrays, name)
    sch2 = getschema(tonumpy(arrays, **{name: sch}), name)
    if debug:
        print(sch2)
    assert sch == sch2
        
assert schema(None) == {"unknown"}
assert schema(True) == {"boolean"}
assert schema(False) == {"boolean"}
assert schema(3) == {"integer"}
assert schema(3.14) == {"number"}
assert schema("hello") == {"string"}
assert schema([]) == {"sequence": {"unknown"}}
assert schema([None]) == {"sequence": {"unknown"}}
assert schema([True]) == {"sequence": {"boolean"}}
assert schema([True, False]) == {"sequence": {"boolean"}}
try:
    schema([True, False, 3])
except TypeError:
    pass
else:
    assert False
assert schema([3]) == {"sequence": {"integer"}}
assert schema([3, 4]) == {"sequence": {"integer"}}
assert schema([3, 4.4]) == {"sequence": {"number"}}
assert schema([3.3]) == {"sequence": {"number"}}
assert schema([3.3, 4.4]) == {"sequence": {"number"}}
assert schema(["hello"]) == {"sequence": {"string"}}
assert schema([""]) == {"sequence": {"string"}}
assert schema(["", "hello"]) == {"sequence": {"string"}}
assert schema({}) == {"record": {}}
assert schema({"one": 1}) == {"record": {"one": {"integer"}}}
assert schema({"one": 1, "two": 2.2, "three": "THREE"}) == {"record": {"one": {"integer"}, "two": {"number"}, "three": {"string"}}}
assert schema({"one": 1, "two": []}) == {"record": {"one": {"integer"}, "two": {"sequence": {"unknown"}}}}
assert schema({"one": 1, "two": [1]}) == {"record": {"one": {"integer"}, "two": {"sequence": {"integer"}}}}
assert schema({"one": 1, "two": [1, 2.2]}) == {"record": {"one": {"integer"}, "two": {"sequence": {"number"}}}}
try:
    schema({"one": 1, "two": [1, 2.2, "three"]})
except TypeError:
    pass
else:
    assert False
assert schema([{}]) == {"sequence": {"record": {}}}
assert schema([{"one": 1}]) == {"sequence": {"record": {"one": {"integer"}}}}
assert schema([{"one": 1, "two": 2.2, "three": "THREE"}]) == {"sequence": {"record": {"one": {"integer"}, "two": {"number"}, "three": {"string"}}}}
assert schema([{"one": 1}, {"two": 2.2}, {"three": "THREE"}]) == {"sequence": {"record": {"one": {"integer"}, "two": {"number"}, "three": {"string"}}}}
assert schema([{"one": 1}, {"two": []}, {"two": []}]) == {"sequence": {"record": {"one": {"integer"}, "two": {"sequence": {"unknown"}}}}}
assert schema([{"one": 1}, {"two": [1]}, {"two": []}]) == {"sequence": {"record": {"one": {"integer"}, "two": {"sequence": {"integer"}}}}}
assert schema([{"one": 1}, {"two": []}, {"two": [1]}]) == {"sequence": {"record": {"one": {"integer"}, "two": {"sequence": {"integer"}}}}}
assert schema([{"one": 1}, {"two": [1]}, {"two": [2.2]}]) == {"sequence": {"record": {"one": {"integer"}, "two": {"sequence": {"number"}}}}}
try:
    schema([{"one": 1}, {"two": [1]}, {"two": ["hello"]}])
except TypeError:
    pass
else:
    assert False

assert satisfies(None, {"unknown"})
assert satisfies(True, {"boolean"})
assert satisfies(False, {"boolean"})
assert satisfies(3, {"integer"})
assert satisfies(3, {"number"})
assert satisfies(3.14, {"number"})
assert satisfies("hello", {"string"})
assert satisfies([], {"sequence": {"unknown"}})
assert satisfies([None], {"sequence": {"unknown"}})
assert satisfies([True], {"sequence": {"boolean"}})
assert satisfies([True, False], {"sequence": {"boolean"}})
assert satisfies([3], {"sequence": {"integer"}})
assert satisfies([3], {"sequence": {"number"}})
assert satisfies([3, 4], {"sequence": {"integer"}})
assert satisfies([3, 4.4], {"sequence": {"number"}})
assert satisfies([3.3], {"sequence": {"number"}})
assert satisfies([3.3, 4.4], {"sequence": {"number"}})
assert satisfies(["hello"], {"sequence": {"string"}})
assert satisfies([""], {"sequence": {"string"}})
assert satisfies(["", "hello"], {"sequence": {"string"}})
assert satisfies({}, {"record": {}})
assert satisfies({"one": 1}, {"record": {"one": {"integer"}}})
assert satisfies({"one": 1}, {"record": {"one": {"number"}}})
assert satisfies({"one": 1, "two": 2.2, "three": "THREE"}, {"record": {"one": {"integer"}, "two": {"number"}, "three": {"string"}}})
assert satisfies({"one": 1, "two": 2.2, "three": "THREE"}, {"record": {"one": {"number"}, "two": {"number"}, "three": {"string"}}})
assert satisfies({"one": 1, "two": []}, {"record": {"one": {"integer"}, "two": {"sequence": {"unknown"}}}})
assert satisfies({"one": 1, "two": [1]}, {"record": {"one": {"integer"}, "two": {"sequence": {"integer"}}}})
assert satisfies({"one": 1, "two": [1, 2.2]}, {"record": {"one": {"integer"}, "two": {"sequence": {"number"}}}})
assert satisfies([{}], {"sequence": {"record": {}}})
assert satisfies([{"one": 1}], {"sequence": {"record": {"one": {"integer"}}}})
assert satisfies([{"one": 1}], {"sequence": {"record": {"one": {"number"}}}})
assert satisfies([{"one": 1, "two": 2.2, "three": "THREE"}], {"sequence": {"record": {"one": {"integer"}, "two": {"number"}, "three": {"string"}}}})
assert satisfies([{"one": 1}, {"two": 2.2}, {"three": "THREE"}], {"sequence": {"record": {"one": {"integer"}, "two": {"number"}, "three": {"string"}}}})
assert satisfies([{"one": 1}, {"two": []}, {"two": []}], {"sequence": {"record": {"one": {"integer"}, "two": {"sequence": {"unknown"}}}}})
assert satisfies([{"one": 1}, {"two": [1]}, {"two": []}], {"sequence": {"record": {"one": {"integer"}, "two": {"sequence": {"integer"}}}}})
assert satisfies([{"one": 1}, {"two": [1]}, {"two": []}], {"sequence": {"record": {"one": {"integer"}, "two": {"sequence": {"number"}}}}})
assert satisfies([{"one": 1}, {"two": []}, {"two": [1]}], {"sequence": {"record": {"one": {"integer"}, "two": {"sequence": {"integer"}}}}})
assert satisfies([{"one": 1}, {"two": []}, {"two": [1]}], {"sequence": {"record": {"one": {"integer"}, "two": {"sequence": {"number"}}}}})
assert satisfies([{"one": 1}, {"two": [1]}, {"two": [2.2]}], {"sequence": {"record": {"one": {"integer"}, "two": {"sequence": {"number"}}}}})

roundtrip(True, {"x": [1]}, True)
roundtrip(False, {"x": [0]}, False)
roundtrip(3, {"x": [3]}, 3)
roundtrip(3.14, {"x": [3.14]}, 3.14)
roundtrip("hello", {"x$": [104, 101, 108, 108, 111], "x$@size": [5]}, "hello")
roundtrip([True], {"x[]": [1], "x[]@size": [1]}, [True])
roundtrip([True, False], {"x[]": [1, 0], "x[]@size": [2]}, [True, False])
roundtrip([3], {"x[]": [3], "x[]@size": [1]}, [3])
roundtrip([3, 4], {"x[]": [3, 4], "x[]@size": [2]}, [3, 4])
roundtrip([3, 4.4], {"x[]": [3.0, 4.4], "x[]@size": [2]}, [3.0, 4.4])
roundtrip([3.3], {"x[]": [3.3], "x[]@size": [1]}, [3.3])
roundtrip([3.3, 4.4], {"x[]": [3.3, 4.4], "x[]@size": [2]}, [3.3, 4.4])
roundtrip(["hello"], {"x[]$": [104, 101, 108, 108, 111], "x[]$@size": [1, 5]}, ["hello"])
roundtrip([""], {"x[]$": [], "x[]$@size": [1, 0]}, [""])
roundtrip(["", "hello"], {"x[]$": [104, 101, 108, 108, 111], "x[]$@size": [2, 0, 5]}, ["", "hello"])
roundtrip({}, {}, {})
roundtrip({"one": 1}, {"x-one": [1]}, {"one": 1})
roundtrip({"one": 1, "two": 2.2, "three": "THREE"}, {"x-one": [1], "x-two": [2.2], "x-three$": [84, 72, 82, 69, 69], "x-three$@size": [5]}, {"one": 1, "two": 2.2, "three": "THREE"})
roundtrip({"one": 1, "two": [1]}, {"x-one": [1], "x-two[]": [1], "x-two[]@size": [1]}, {"one": 1, "two": [1]})
roundtrip({"one": 1, "two": [1, 2.2]}, {"x-one": [1], "x-two[]": [1.0, 2.2], "x-two[]@size": [2]}, {"one": 1, "two": [1.0, 2.2]})
roundtrip([{"one": 1}], {"x[]-one": [1], "x[]@size": [1]}, [{"one": 1}])
roundtrip([{"one": 1, "two": 2.2, "three": "THREE"}], {"x[]-one": [1], "x[]-two": [2.2], "x[]-three$": [84, 72, 82, 69, 69], "x[]@size": [1], "x[]-three$@size": [1, 5]}, [{"one": 1, "two": 2.2, "three": "THREE"}])
roundtrip([{"one": 1}, {"two": 2.2}, {"three": "THREE"}], {"x[]-one": [1, intnan, intnan], "x[]-two": [floatnan, 2.2, floatnan], "x[]-three$": [84, 72, 82, 69, 69], "x[]@size": [3], "x[]-three$@size": [3, -1, -1, 5]}, [{"one": 1, "two": None, "three": None}, {"one": None, "two": 2.2, "three": None}, {"one": None, "two": None, "three": "THREE"}])
roundtrip([{"one": 1}, {"two": [1]}, {"two": []}], {"x[]-one": [1, intnan, intnan], "x[]-two[]": [1], "x[]@size": [3], "x[]-two[]@size": [3, -1, 1, 0]}, [{"one": 1, "two": None}, {"one": None, "two": [1]}, {"one": None, "two": []}])
roundtrip([{"one": 1}, {"two": []}, {"two": [1]}], {"x[]-one": [1, intnan, intnan], "x[]-two[]": [1], "x[]@size": [3], "x[]-two[]@size": [3, -1, 0, 1]}, [{"one": 1, "two": None}, {"one": None, "two": []}, {"one": None, "two": [1]}])
roundtrip([{"one": 1}, {"two": [1]}, {"two": [2.2]}], {"x[]-one": [1, intnan, intnan], "x[]-two[]": [1.0, 2.2], "x[]@size": [3], "x[]-two[]@size": [3, -1, 1, 1]}, [{"one": 1, "two": None}, {"one": None, "two": [1.0]}, {"one": None, "two": [2.2]}])

schema2name(True)
schema2name(False)
schema2name(3)
schema2name(3.14)
schema2name("hello")
schema2name([True])
schema2name([True, False])
schema2name([3])
schema2name([3, 4])
schema2name([3, 4.4])
schema2name([3.3])
schema2name([3.3, 4.4])
schema2name(["hello"])
schema2name([""])
schema2name(["", "hello"])
schema2name({})
schema2name({"one": 1})
schema2name({"one": 1, "two": 2.2, "three": "THREE"})
schema2name({"one": 1, "two": [1]})
schema2name({"one": 1, "two": [1, 2.2]})
schema2name([{"one": 1}])
schema2name([{"one": 1, "two": 2.2, "three": "THREE"}])
schema2name([{"one": 1}, {"two": 2.2}, {"three": "THREE"}])
schema2name([{"one": 1}, {"two": [1]}, {"two": []}])
schema2name([{"one": 1}, {"two": []}, {"two": [1]}])
schema2name([{"one": 1}, {"two": [1]}, {"two": [2.2]}])

def randomschema():
    base = random.choice(["boolean", "integer", "number", "string", "sequence", "record"])
    if base == "sequence":
        return {"sequence": randomschema()}
    elif base == "record":
        return {"record": {fn: randomschema() for fn in ["one", "two", "three", "four", "five"][:random.randint(1, 5)]}}
    else:
        return {base}

def randomvalue(sch):
    if sch == {"boolean"}:
        return random.choice([False, True])
    elif sch == {"integer"}:
        return random.randint(-1000, 1000)
    elif sch == {"number"}:
        return random.uniform(-1000, 1000)
    elif sch == {"string"}:
        return random.choice(["good", "morning", "to", "all", "you", "people"])
    elif generic(sch) == "sequence":
        return [randomvalue(param(sch)) for i in range(random.randint(0, 6))]
    elif generic(sch) == "record":
        return {n: randomvalue(s) for n, s in param(sch).items()}
    else:
        assert False, "schema is {}".format(sch)

# for i in range(100):
#     name = "x"
#     sch = randomschema()
#     obj = randomvalue(sch)
    
#     arrays = newarrays(sch, name)
#     toflat(obj, sch, arrays, name)
#     sch2 = getschema(tonumpy(arrays, **{name: sch}), name)
#     result = fromflat(arrays, sch, name)

#     everything = """sch    = {}
# sch2   = {}
# input  = {}
# output = {}
# arrays = {}
# """.format(sch, sch2, obj, result, arrays)

#     assert sch == sch2, everything
#     assert result == obj, everything

