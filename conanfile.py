from conans import ConanFile, CMake, tools, Meson
import os

class GstpluginsgoodConan(ConanFile):
    name = "gst-plugins-good-1.0"
    version = "1.14.4"
    description = "'Good' GStreamer plugins and helper libraries"
    url = "https://github.com/conanos/gst-plugins-good-1.0"
    homepage = "https://github.com/GStreamer/gst-plugins-good"
    license = "GPLv2+"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"
    requires = ("gstreamer-1.0/1.14.4@conanos/dev","gst-plugins-base-1.0/1.14.4@conanos/dev","libjpeg-turbo/1.5.2@conanos/dev",
                "libpng/1.6.34@conanos/dev","speex/1.2rc2@conanos/dev", "gdk-pixbuf/2.36.2@conanos/dev", "libsoup/2.62.3@conanos/dev",
                "mpg123/1.25.10@conanos/dev", "lame/3.100@conanos/dev", "orc/0.4.28@conanos/dev","wavpack/5.1.0@conanos/dev",
                "flac/1.3.2@conanos/dev", "taglib/1.11.1@conanos/dev", "bzip2/1.0.6@conanos/dev", "zlib/1.2.11@conanos/dev",
                "libvpx/1.7.0@conanos/dev", "libdv/1.0.0@conanos/dev", "cairo/1.14.12@conanos/dev","gobject-introspection/1.58.0@conanos/dev",

                "libffi/3.3-rc0@conanos/dev","glib/2.58.0@conanos/dev","libxml2/2.9.8@conanos/dev","glib-networking/2.58.0@conanos/dev",
                "sqlite3/3.21.0@conanos/dev",)

    source_subfolder = "source_subfolder"
    remotes = {'origin': 'https://github.com/GStreamer/gst-plugins-good.git'}

    def source(self):
        #tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version))
        #extracted_dir = "gst-plugins-good-" + self.version
        #os.rename(extracted_dir, self.source_subfolder)
        tools.mkdir(self.source_subfolder)
        with tools.chdir(self.source_subfolder):
            self.run('git init')
            for key, val in self.remotes.items():
                self.run("git remote add %s %s"%(key, val))
            self.run('git fetch --all')
            self.run('git reset --hard %s'%(self.version))
            self.run('git submodule update --init --recursive')

    def build(self):
        with tools.chdir(self.source_subfolder):
            with tools.environment_append({
                'C_INCLUDE_PATH':'%s/include:%s/include:%s/include/libsoup-2.4'%(self.deps_cpp_info["bzip2"].rootpath,
                self.deps_cpp_info["libjpeg-turbo"].rootpath,self.deps_cpp_info["libsoup"].rootpath),
                'LIBRARY_PATH':'%s/lib:%s/lib:%s/lib'%(self.deps_cpp_info["bzip2"].rootpath,
                self.deps_cpp_info["libjpeg-turbo"].rootpath,self.deps_cpp_info["lame"].rootpath),
                'PATH':'%s/bin:%s/bin:%s'%(self.deps_cpp_info["orc"].rootpath,self.deps_cpp_info["gobject-introspection"].rootpath,os.getenv("PATH")),
                'LD_LIBRARY_PATH':'%s/lib:%s/lib'%(self.deps_cpp_info["libffi"].rootpath,self.deps_cpp_info["sqlite3"].rootpath)
                }):

                meson = Meson(self)
                _defs = {'prefix':'%s/builddir/install'%(os.getcwd()), 'libdir':'lib','use_orc':'yes'}
                meson.configure(
                    defs=_defs,
                    source_dir = '%s'%(os.getcwd()),
                    build_dir= '%s/builddir'%(os.getcwd()),
                    pkg_config_paths=['%s/lib/pkgconfig'%(self.deps_cpp_info["gstreamer-1.0"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["gst-plugins-base-1.0"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["libjpeg-turbo"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["libpng"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["speex"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["gdk-pixbuf"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["libsoup"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["mpg123"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["lame"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["orc"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["wavpack"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["flac"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["taglib"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["bzip2"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["zlib"].rootpath),#required by gobject
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["libvpx"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["libdv"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["cairo"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["libffi"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["gobject-introspection"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["glib"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["libxml2"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["glib-networking"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["sqlite3"].rootpath),
                                      ]
                                )
                meson.build(args=['-j2'])
                self.run('ninja -C {0} install'.format(meson.build_dir))

    def package(self):
        if tools.os_info.is_linux:
            with tools.chdir(self.source_subfolder):
                self.copy("*", src="%s/builddir/install"%(os.getcwd()))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

