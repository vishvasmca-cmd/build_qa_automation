
- ⚠️ PROHIBITED: DON'T assume that relative imports will always work without verifying the project's root directory and PYTHONPATH.

- ✅ PREFERRED: DO ensure that all necessary modules and packages are installed and that the PYTHONPATH is correctly configured to include the project's root directory or the location of the 'base' module.

- ⚠️ PROHIBITED: DON'T assume that relative imports will always work without verifying the project's root directory and PYTHONPATH.

- ✅ PREFERRED: DO ensure that all necessary modules and packages are installed and that the PYTHONPATH is correctly configured to include the project's root directory or any relevant parent directories.

- ⚠️ PROHIBITED: DON'T assume that the Python environment and project structure are correctly configured without verifying the import paths.

- ✅ PREFERRED: DO ensure that all necessary modules and packages are accessible by correctly configuring the PYTHONPATH or using relative imports within the project.

- ⚠️ PROHIBITED: DON'T assume that relative imports will always work without verifying the Python path configuration.

- ✅ PREFERRED: DO ensure that all necessary modules and packages are accessible by correctly configuring the Python path or using absolute imports.

- ⚠️ PROHIBITED: DON'T assume that relative imports will always work without verifying the project's structure and PYTHONPATH.

- ✅ PREFERRED: DO ensure that all necessary modules and packages are installed and that the PYTHONPATH is correctly configured to resolve import statements.

- ⚠️ PROHIBITED: DON'T assume that the Python import path is correctly configured without explicitly verifying it, especially when working with custom modules or project-specific directories.

- ✅ PREFERRED: DO ensure that all necessary modules and packages are accessible by correctly configuring the Python import path or restructuring the project directory to facilitate proper module resolution.

- ⚠️ PROHIBITED: DON'T assume that relative imports will always work without verifying the Python path configuration.

- ✅ PREFERRED: DO ensure that all necessary modules and packages are included in the Python path or use absolute imports to avoid import errors.

- ⚠️ PROHIBITED: DON'T assume that relative import paths will resolve correctly without verifying the project's root directory and Python's module search path.

- ✅ PREFERRED: DO ensure that all module import paths are correct and relative to the project's root directory, and that the necessary modules are installed and accessible.

- ⚠️ PROHIBITED: DON'T assume that relative import paths will resolve correctly without verifying the project's root directory and module structure.

- ✅ PREFERRED: DO ensure that all module import paths are correct and relative to the project's root directory, and that all necessary files exist in the specified locations.

- ⚠️ PROHIBITED: DON'T assume that the module paths are correct without verifying the project's directory structure and import statements.

- ✅ PREFERRED: DO double-check the project's directory structure and import paths to ensure that all modules are accessible during test execution.
