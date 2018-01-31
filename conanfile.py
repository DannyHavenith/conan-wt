from conans import ConanFile, CMake, tools


class WtConan(ConanFile):
    name = "wt"
    version = "4.0.2"
    license = "GPL2"
    url = "."
    description = "Wt, C++ Web Toolkit http://www.webtoolkit.eu/wt"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    requires = "Boost/1.64.0@conan/stable"
    default_options = "shared=True", "Boost:shared=True", "Boost:fPIC=True"
    generators = "cmake"

    def source(self):
        self.run("git clone --depth=1 --branch " + self.version + " git@github.com:emweb/wt.git")
        self.run("cd wt")
        useCxxAbi = 0
        if self.settings.os != "Android":
            try:
                if str(self.settings.compiler.libcxx) == "libstdc++":
                    useCxxAbi = 0
                elif str(self.settings.compiler.libcxx) == "libstdc++11":
                    useCxxAbi = 1
            except:
                pass
                
        tools.replace_in_file("wt/CMakeLists.txt", "PROJECT(WT)", '''PROJECT(WT)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
''')

        # Running- and linking to boost unit test framework is a major pain. Hence, hack them out of this build.
        tools.replace_in_file("wt/CMakeLists.txt", 'OPTION(BUILD_TESTS "Build Wt tests" ON)', 'OPTION(BUILD_TESTS "Build Wt tests" OFF)')


    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="wt")
        cmake.build( target="install")

        # Explicit way:
        # self.run('cmake %s/hello %s' % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy( "*", src="package")

    def package_info(self):
        self.cpp_info.libs = ["wthttp", "wt"]
