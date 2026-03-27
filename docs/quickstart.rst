.. _quickstart:

Quickstart
==========

After you have downloaded and installed PyCantonese (see :ref:`download_install`),
import the package ``pycantonese`` in your Python interpreter:

.. code-block:: python

    import pycantonese

No errors? Great! Now you're ready to proceed.

1. Word segmentation

.. code-block:: python

    pycantonese.segment("廣東話好難學？")  # Is Cantonese difficult to learn?
    # ['廣東話', '好', '難學', '？']

2. Conversion from Cantonese characters to Jyutping

.. code-block:: python

    pycantonese.characters_to_jyutping('香港人講廣東話')  # Hongkongers speak Cantonese
    # [('香港人', 'hoeng1gong2jan4'), ('講', 'gong2'), ('廣東話', 'gwong2dung1waa2')]

3. Finding all verbs in the HKCanCor corpus

   In this example,
   we search for the regular expression ``'^[Vv]'`` for all words whose
   part-of-speech tag begins with "v" (or "V" for morpheme tags) in the
   original HKCanCor annotations:

.. code-block:: python

    corpus = pycantonese.hkcancor() # get HKCanCor
    all_verbs = corpus.search(pos='^[Vv]')
    len(all_verbs)  # number of all verbs
    # 29726
    all_verbs[:10]  ## print 10 results
    # [Token(word='去', pos='v', jyutping='heoi3', mor=None, gloss=None, gra=None),
    #  Token(word='去', pos='v', jyutping='heoi3', mor=None, gloss=None, gra=None),
    #  Token(word='旅行', pos='vn', jyutping='leoi5hang4', mor=None, gloss=None, gra=None),
    #  Token(word='有冇', pos='v1', jyutping='jau5mou5', mor=None, gloss=None, gra=None),
    #  Token(word='要', pos='vu', jyutping='jiu3', mor=None, gloss=None, gra=None),
    #  Token(word='有得', pos='vu', jyutping='jau5dak1', mor=None, gloss=None, gra=None),
    #  Token(word='冇得', pos='vu', jyutping='mou5dak1', mor=None, gloss=None, gra=None),
    #  Token(word='去', pos='v', jyutping='heoi3', mor=None, gloss=None, gra=None),
    #  Token(word='係', pos='v', jyutping='hai6', mor=None, gloss=None, gra=None),
    #  Token(word='係', pos='v', jyutping='hai6', mor=None, gloss=None, gra=None)]

4. Parsing Jyutping for the onset, nucleus, coda, and tone

.. code-block:: python

    pycantonese.parse_jyutping('gwong2dung1waa2')  # 廣東話
    # [Jyutping(onset='gw', nucleus='o', coda='ng', tone='2'),
    #  Jyutping(onset='d', nucleus='u', coda='ng', tone='1'),
    #  Jyutping(onset='w', nucleus='aa', coda='', tone='2')]

Looking for more functionality?
Please use the documentation menu on the left.

.. _javascript:

Using PyCantonese in JavaScript
-------------------------------

PyCantonese can run entirely in the browser or in Node.js via
`Pyodide <https://pyodide.org>`_, a Python runtime compiled to WebAssembly.
This means you can use PyCantonese without a server-side Python backend.

**Setup**

WASM wheels are attached to each GitHub release of
`Rustling <https://github.com/jacksonllee/rustling/releases>`_ and
`PyCantonese <https://github.com/jacksonllee/pycantonese/releases>`_
(the ``.whl`` files with ``emscripten`` in the filename).
PyCantonese depends on Rustling, so both wheels are needed.
Install them directly from the GitHub release URLs using ``micropip``.

**Browser example**

.. code-block:: html

    <!DOCTYPE html>
    <html>
    <head>
      <script src="https://cdn.jsdelivr.net/pyodide/v0.27.5/full/pyodide.js"></script>
    </head>
    <body>
      <script>
        async function main() {
          const pyodide = await loadPyodide();

          // Update these version numbers as needed.
          const RUSTLING_VERSION = "0.8.0";
          const PYCANTONESE_VERSION = "4.2.0";
          const EMSCRIPTEN_TAG = "cp310-abi3-emscripten_4_0_9_wasm32";

          await pyodide.loadPackage("micropip");
          const micropip = pyodide.pyimport("micropip");
          await micropip.install(
            `https://github.com/jacksonllee/rustling/releases/download/v${RUSTLING_VERSION}/rustling-${RUSTLING_VERSION}-${EMSCRIPTEN_TAG}.whl`
          );
          await micropip.install(
            `https://github.com/jacksonllee/pycantonese/releases/download/v${PYCANTONESE_VERSION}/pycantonese-${PYCANTONESE_VERSION}-${EMSCRIPTEN_TAG}.whl`
          );

          // Use PyCantonese from JavaScript.
          const result = pyodide.runPython(`
            import pycantonese
            print(pycantonese.characters_to_jyutping("香港人講廣東話"))
          `);
        }
        main();
      </script>
    </body>
    </html>

**Node.js example**

.. code-block:: javascript

    const { loadPyodide } = require("pyodide");

    async function main() {
      const pyodide = await loadPyodide();
      await pyodide.loadPackage("micropip");
      const micropip = pyodide.pyimport("micropip");

      // Update these version numbers as needed.
      const RUSTLING_VERSION = "0.8.0";
      const PYCANTONESE_VERSION = "4.2.0";
      const EMSCRIPTEN_TAG = "cp310-abi3-emscripten_4_0_9_wasm32";

      await micropip.install(
        `https://github.com/jacksonllee/rustling/releases/download/v${RUSTLING_VERSION}/rustling-${RUSTLING_VERSION}-${EMSCRIPTEN_TAG}.whl`
      );
      await micropip.install(
        `https://github.com/jacksonllee/pycantonese/releases/download/v${PYCANTONESE_VERSION}/pycantonese-${PYCANTONESE_VERSION}-${EMSCRIPTEN_TAG}.whl`
      );

      const jyutping = pyodide.runPython(`
        import pycantonese
        pycantonese.characters_to_jyutping("香港人講廣東話")
      `);
      console.log(jyutping.toJs());
      // [['香港人', 'hoeng1gong2jan4'], ['講', 'gong2'], ['廣東話', 'gwong2dung1waa2']]
    }

    main();

**Notes**

- The URLs contain version numbers. Update them when using a different release.
- Parallelization is automatically disabled in the Pyodide environment,
  since WebAssembly does not support multithreading.
  Single-threaded performance is otherwise the same.
- All PyCantonese functions (word segmentation, Jyutping conversion, corpus access, etc.)
  are available in Pyodide.
