#! /usr/bin/env python
import aipy as a, numpy as n, pylab as p
import sys, optparse

o = optparse.OptionParser()
#a.scripting.add_standard_options(o, cal=True)
#o.add_option('--aspect_neq', action='store_true', help='Do not force equal aspect in x/y plot.')
opts, args = o.parse_args(sys.argv[1:])

CALFILE='psa6240_v003'

p.figure(figsize=(6.5,5.4))
th = n.arange(0, 2*n.pi, .01)
r = 5.
aa = a.cal.get_aa(CALFILE, .1, .1, 1)
antpos = [aa.get_baseline(0,i,src='z') for i in range(len(aa.ants))]
antpos = n.array(antpos) * a.const.len_ns / 100.
x,y,z = antpos[:,0], antpos[:,1], antpos[:,2]
x -= n.average(x)
y -= n.average(y)
p.plot(x,y, 'k.')
p.xlim(n.min(x) - 10, n.max(x) + 10)
p.ylim(n.min(y) - 10, n.max(y) + 10)
#Draw lines for baselines 49_41, 49_3, 10_41
fiducialx = (x[49],x[41])
fiducialy = (y[49],y[41])
p.plot(fiducialx,fiducialy, 'k-', linewidth=1.5)
fiducial2x = (x[49],x[3])
fiducial2y = (y[49],y[3])
p.plot(fiducial2x,fiducial2y, '-', color=(0.,107./255, 164./255), linewidth=1.5)
fiducial3x = (x[10],x[41])
fiducial3y = (y[10],y[41])
p.plot(fiducial3x,fiducial3y, '-', color=(1.,128./255,14./255), linewidth=1.5)
if False:
    im = a.img.Img(size=300, res=30)
    DIM = 300./30
    im.put((x,y,z), z)
    _z = a.img.recenter(im.uv, (DIM/2,DIM/2))
    print _z
    _z = n.ma.array(_z, mask=n.where(_z == 0, 1, 0))
    _x,_y = im.get_uv()
    _x = a.img.recenter(_x, (DIM/2,DIM/2))
    _y = a.img.recenter(_y, (DIM/2,DIM/2))
    p.contourf(_x,_y,_z,n.arange(-5,5,.5))
for ant,(xa,ya,za) in enumerate(zip(x,y,z)):
    hx,hy = r*za*n.cos(th)+xa, r*za*n.sin(th)+ya
    if za > 0: fmt = '#eeeeee'
    else: fmt = '#a0a0a0'
#    p.fill(hx,hy, fmt)
    p.text(xa,ya, str(ant),size='large')
p.grid()
#p.xlim(-100,100)
p.xlabel("East-West Antenna Position (m)", fontsize='large')
p.ylabel("North-South Antenna Position (m)", fontsize='large')
#p.ylim(-100,100)
a = p.gca()
#if not opts.aspect_neq: a.set_aspect('equal')
p.savefig('antenna_positions.png', format='png')
p.show()
