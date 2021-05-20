\ Model P6
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  210000 vessel1 + 285000 vessel2 + 0.04 dLoaded(1) + 0.032 dLoaded(2)
   + 0.0336 dEmpty(1) + 0.024 dEmpty(2)
Subject To
 c1: 35 trips(9,1) + 35 trips(10,1) + 35 trips(11,1) + 35 trips(12,1)
   + 70 trips(9,2) + 70 trips(10,2) + 70 trips(11,2) + 70 trips(12,2)
   >= 50000
 c2: 35 trips(1,1) + 35 trips(2,1) + 35 trips(3,1) + 35 trips(4,1)
   + 35 trips(5,1) + 35 trips(6,1) + 35 trips(7,1) + 35 trips(8,1)
   + 70 trips(6,2) + 70 trips(7,2) + 70 trips(8,2) >= 40000
 c3: 35 trips(9,1) + 35 trips(10,1) + 35 trips(11,1) + 35 trips(12,1)
   + 70 trips(9,2) + 70 trips(10,2) + 70 trips(11,2) + 70 trips(12,2)
   >= 50000
 c4: 35 trips(1,1) + 35 trips(3,1) + 35 trips(5,1) + 35 trips(7,1)
   + 70 trips(7,2) >= 20000
 c5: 35 trips(2,1) + 35 trips(4,1) + 35 trips(6,1) + 35 trips(8,1)
   + 70 trips(6,2) + 70 trips(8,2) >= 20000
 c6: 35 trips(2,1) + 35 trips(6,1) + 35 trips(10,1) + 35 trips(11,1)
   + 70 trips(6,2) + 70 trips(10,2) + 70 trips(11,2) >= 30000
 c7: 35 trips(10,1) + 35 trips(12,1) + 70 trips(10,2) + 70 trips(12,2)
   - load(Mars,Wheat) >= 0
 c8: load(Mars,Wheat) <= 40000
 c9: 35 trips(5,1) + 35 trips(6,1) + 35 trips(7,1) + 35 trips(8,1)
   + 70 trips(6,2) + 70 trips(7,2) + 70 trips(8,2) - load(Mars,Corn) >= 0
 c10: load(Mars,Corn) <= 20000
 c11: 35 trips(3,1) + 35 trips(7,1) + 70 trips(7,2) >= 10000
 c12: 35 trips(4,1) + 35 trips(8,1) + 35 trips(9,1) + 35 trips(12,1)
   + 70 trips(8,2) + 70 trips(9,2) + 70 trips(12,2) >= 40000
 c13: 35 trips(9,1) + 35 trips(11,1) + 70 trips(9,2) + 70 trips(11,2)
   - load(Sky,Wheat) >= 0
 c14: 35 trips(1,1) + 35 trips(5,1) >= 10000
 c15: 35 trips(1,1) + 35 trips(2,1) + 35 trips(3,1) + 35 trips(4,1)
   - load(Moon,Corn) >= 0
 c16: load(Mars,Wheat) + load(Sky,Wheat) = 50000
 c17: load(Mars,Corn) + load(Moon,Corn) = 40000
 c18: - 8280 vessel1 + 400 trips(1,1) + 453.3333333333334 trips(2,1)
   + 456.6666666666666 trips(3,1) + 456.6666666666666 trips(4,1)
   + 453.3333333333334 trips(5,1) + 440 trips(6,1)
   + 526.6666666666667 trips(7,1) + 526.6666666666667 trips(8,1)
   + 480 trips(9,1) + 384 trips(10,1) + 498.6666666666667 trips(11,1)
   + 498.6666666666667 trips(12,1) <= 0
 c19: - 8280 vessel2 + 550 trips(6,2) + 658.3333333333333 trips(7,2)
   + 658.3333333333333 trips(8,2) + 600 trips(9,2) + 480 trips(10,2)
   + 623.3333333333333 trips(11,2) + 623.3333333333333 trips(12,2) <= 0
 c20: - 10000 trips(1,1) - 10500 trips(2,1) - 11000 trips(3,1)
   - 22000 trips(4,1) - 10500 trips(5,1) - 11000 trips(6,1)
   - 11500 trips(7,1) - 11500 trips(8,1) - 12000 trips(9,1)
   - 9600 trips(10,1) - 10800 trips(11,1) - 10800 trips(12,1) + dLoaded(1)
   = 0
 c21: - 11000 trips(6,2) - 11500 trips(7,2) - 11500 trips(8,2)
   - 12000 trips(9,2) - 9600 trips(10,2) - 10800 trips(11,2)
   - 10800 trips(12,2) + dLoaded(2) = 0
 c22: - 1000 trips(2,1) - 500 trips(3,1) - 500 trips(4,1) - 1000 trips(5,1)
   - 2000 trips(7,1) - 2000 trips(8,1) - 2000 trips(11,1)
   - 2000 trips(12,1) + dEmpty(1) = 0
 c23: - 2000 trips(7,2) - 2000 trips(8,2) - 2000 trips(11,2)
   - 2000 trips(12,2) + dEmpty(2) = 0
Bounds
End
