SET_SOURCE_FILES_PROPERTIES(${SOURCE_FILES} PROPERTIES CYTHON_IS_CXX FALSE)
# 已经在根目录下的CMakeLists.txt中设置了可执行文件，这里就不重复设置
#cython_add_standalone_executable(${PROJECT_NAME} MAIN_MODULE "main.pyx")
