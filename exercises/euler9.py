for x in range(1,1000):
  #print(x)
  for y in range(x,1000):
    for z in range(y,1000):
      if x+y+z == 1000:
        #print(x,y,z)
        if x*x + y*y == z*z:
          print(x,y,z,x*y*z)
          break
