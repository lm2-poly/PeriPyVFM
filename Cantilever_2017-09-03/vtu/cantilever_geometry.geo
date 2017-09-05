lc = 1.0;
// Geometry
Point(1) = {0, -12.5, 0, lc};
Point(2) = {81, -12.5, 0, lc};
Point(3) = {81, 12.5, 0, lc};
Point(4) = {0, 12.5, 0, lc};

Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};

Line Loop(1) = {1, 2, 3, 4};
Plane Surface(1) = {1};

// Meshing
Transfinite Line {1} = 82Using Progression 1;
Transfinite Line {2} = 26Using Progression 1;
Transfinite Line {3} = 82Using Progression 1;
Transfinite Line {4} = 26Using Progression 1;
Transfinite Surface {1};

// Rectangular mesh
Recombine Surface {1};