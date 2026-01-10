
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

- ⚠️ PROHIBITED: DON'T assume that the project's directory structure and import paths are correct without verifying them before running tests.

- ✅ PREFERRED: DO ensure that all necessary modules and packages are installed and that the import paths in the test files are accurate and reflect the project's directory structure.

- ⚠️ PROHIBITED: DON'T assume that relative import paths will resolve correctly without verifying the project's root directory and module structure.

- ✅ PREFERRED: DO ensure that all module import paths are correct and relative to the project's root directory, and that all necessary modules are installed and accessible.

- ⚠️ PROHIBITED: DON'T assume that the Python path is correctly configured; ALWAYS verify module import paths before running tests.

- ✅ PREFERRED: DO ensure that all necessary modules and packages are installed and that the Python path includes the project's root directory or any relevant subdirectories.

- ⚠️ PROHIBITED: DON'T assume that module paths are correct without verifying the file structure and import statements.

- ✅ PREFERRED: DO double-check the file structure and import statements to ensure that all modules are accessible and correctly referenced.

- ⚠️ PROHIBITED: DON'T assume that relative import paths will resolve correctly without verifying the project's root directory and Python's module search path.

- ✅ PREFERRED: DO ensure that all module import paths are correct and relative to the project's root directory, and that the necessary modules are installed and accessible.

- ⚠️ PROHIBITED: DON'T assume that relative imports will work without verifying the project's root directory is correctly configured for pytest.

- ✅ PREFERRED: DO ensure that all module paths used in import statements are accurate and reflect the actual directory structure of the project.

- ⚠️ PROHIBITED: DON'T assume that relative import paths will resolve correctly without verifying the project's root directory and module structure.

- ✅ PREFERRED: DO ensure that all module import paths are correct and that the necessary modules are present in the specified locations before running tests.

- ⚠️ PROHIBITED: DON'T assume that relative import paths will resolve correctly without verifying the project's root directory and Python's module search path.

- ✅ PREFERRED: DO ensure that all module dependencies are correctly installed and that the Python module search path includes the project's root directory or that absolute import paths are used to avoid import errors.

- ⚠️ PROHIBITED: DON'T assume that relative imports will work without verifying the correct project structure and PYTHONPATH configuration.

- ✅ PREFERRED: DO verify the project's directory structure and PYTHONPATH to ensure that all modules can be imported correctly before running tests.

- ⚠️ PROHIBITED: DON'T assume that the module paths are correct without verifying the project's directory structure and import statements.

- ✅ PREFERRED: DO double-check the project's directory structure and import paths to ensure that all modules are accessible before running the tests.

- ⚠️ PROHIBITED: DON'T assume that all required modules are available in the execution environment; ALWAYS verify dependencies and import paths.

- ✅ PREFERRED: DO ensure that all necessary modules and dependencies are installed and that import paths are correctly configured before running tests.

- ⚠️ PROHIBITED: DON'T assume that all required modules are available in the PYTHONPATH; ALWAYS verify module availability before running tests.

- ✅ PREFERRED: DO ensure that all necessary modules, like 'base_page', are correctly placed within the project structure and that the PYTHONPATH is configured to include the module's location.

- ⚠️ PROHIBITED: DON'T assume that all required modules are available in the PYTHONPATH; ALWAYS verify module availability before running tests.

- ✅ PREFERRED: DO ensure that all necessary modules, like 'base_page', are correctly placed within the project structure and that the PYTHONPATH is configured to include the project's root directory.

- ⚠️ PROHIBITED: DON'T assume that all required modules are available in the PYTHONPATH; ALWAYS verify module availability before running tests.

- ✅ PREFERRED: DO ensure that all necessary modules, like 'base_page', are correctly placed within the project structure and that the PYTHONPATH is configured to include the module's location.

- ⚠️ PROHIBITED: DON'T assume that all required modules are available in the PYTHONPATH; ALWAYS verify the import paths and module availability before running tests.

- ✅ PREFERRED: DO ensure that all necessary modules, like 'base_page', are correctly placed within the project structure and that the PYTHONPATH is configured to include the relevant directories.

- ⚠️ PROHIBITED: DON'T assume that all dependencies are available in the execution environment without explicitly verifying their presence and correct path configuration.

- ✅ PREFERRED: DO ensure that all required modules and dependencies are installed and accessible in the Python environment before running the tests. Verify the PYTHONPATH and relative/absolute import paths.

- ⚠️ PROHIBITED: DON'T assume that all dependencies are automatically available; ALWAYS verify the Python environment and project structure before running tests.

- ✅ PREFERRED: DO ensure that all required modules are installed and that the Python environment is correctly configured with the appropriate PYTHONPATH or virtual environment settings.

- ⚠️ PROHIBITED: DON'T assume that all required modules are available in the execution environment; ALWAYS verify dependencies and import paths.

- ✅ PREFERRED: DO ensure that all necessary modules are installed and that the PYTHONPATH is correctly configured before running tests.

- ⚠️ PROHIBITED: DON'T assume that all dependencies are available in the test environment; ALWAYS verify the presence and correct path of all required modules before running tests.

- ✅ PREFERRED: DO use a robust dependency management system (e.g., `pip install -r requirements.txt`) to ensure all required modules are installed before running tests. DO also use absolute imports or configure PYTHONPATH to avoid relative path issues.

- ⚠️ PROHIBITED: DON'T assume that all required modules are accessible without explicitly verifying the Python import path configuration.

- ✅ PREFERRED: DO ensure that all dependent modules are correctly placed within the project structure and that the Python import path is configured to include the location of these modules.
