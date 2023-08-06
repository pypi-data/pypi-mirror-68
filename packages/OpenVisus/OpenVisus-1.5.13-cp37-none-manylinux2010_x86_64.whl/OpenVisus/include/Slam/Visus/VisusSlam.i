%module(directors="1") VisusSlamPy

%{
#include <Visus/Kernel.h>
#include <Visus/VisusSlam.h>
using namespace Visus;
%}

%include <Visus/VisusPy.i>

%feature("director") Visus::Slam;

%apply SWIGTYPE* DISOWN {Visus::Camera* disown};

%template(VectorOfCamera)     std::vector<Visus::Camera*>;
%template(VectorOfMatch)      std::vector<Visus::Match>;
%template(VectorOfKeyPoint)   std::vector<Visus::KeyPoint>;

// you can do also: (scrgiorgio, does it work?)
// %import(module="OpenVisus.VisusKernelPy") <Visus/VisusKernelPy.i>

%import <Visus/VisusKernelPy.i>
%include <Visus/VisusSlam.h>


