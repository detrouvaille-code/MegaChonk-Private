"""Original seated character modeled from the user's IMG_0664.jpg turnaround.

Run in a SEPARATE Blender 3.4+ process with --background --factory-startup.
Writes only assets/models/artist-work/tactical-tabby; never loads the game cat.
The authored mesh, modest posing rig and clips are an artist candidate, not a
replacement for the active Turkish Van or its tested gameplay animation set.
"""
import bpy
import math
import os
import json
import random
import struct
import sys
from mathutils import Vector

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = os.path.join(ROOT, 'assets', 'models', 'artist-work', 'tactical-tabby')
if '--output-dir' in sys.argv:
    OUT = os.path.abspath(sys.argv[sys.argv.index('--output-dir')+1])
PREV = os.path.join(OUT, 'previews')
os.makedirs(PREV, exist_ok=True)
random.seed(664)
PARTS = []
WEIGHTS = {}


def linear(c):
    return c / 12.92 if c < .04045 else ((c + .055) / 1.055) ** 2.4


def rgb(h):
    return tuple(linear(int(h[i:i+2], 16) / 255) for i in (0, 2, 4)) + (1,)


def material(name, color, roughness=.65, metal=0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = rgb(color)
    m.use_nodes = True
    p = m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = m.diffuse_color
    p.inputs['Roughness'].default_value = roughness
    p.inputs['Metallic'].default_value = metal
    return m


def finish(obj, name, mat, bone='Head'):
    obj.name = name
    if mat: obj.data.materials.append(mat)
    for poly in obj.data.polygons: poly.use_smooth = True
    PARTS.append(obj)
    WEIGHTS[obj.name] = bone
    return obj


def mesh(name, verts, faces, mat, bone='Head'):
    data = bpy.data.meshes.new(name)
    data.from_pydata(verts, [], faces)
    data.update()
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    return finish(obj, name, mat, bone)


def apply_transforms(obj):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


def ellipsoid(name, center, scale, mat, bone='Head', segments=48, rings=28):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=center)
    obj = bpy.context.object
    obj.scale = scale
    apply_transforms(obj)
    return finish(obj, name, mat, bone)


def box(name, center, dimensions, radius, mat, bone='Chest', rotation=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=center)
    obj = bpy.context.object
    obj.scale = dimensions
    obj.rotation_euler = rotation
    apply_transforms(obj)
    bevel = obj.modifiers.new('Soft sewn edges', 'BEVEL')
    bevel.width = radius
    bevel.segments = 4
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=bevel.name)
    obj.data.use_auto_smooth = True
    norm = obj.modifiers.new('Panel normals', 'WEIGHTED_NORMAL')
    bpy.ops.object.modifier_apply(modifier=norm.name)
    return finish(obj, name, mat, bone)


def tube(name, points, radius, mat, bone='Head', cyclic=False):
    curve = bpy.data.curves.new(name, 'CURVE')
    curve.dimensions = '3D'
    curve.resolution_u = 12
    curve.bevel_depth = radius
    curve.bevel_resolution = 3
    curve.use_fill_caps = True
    sp = curve.splines.new('BEZIER')
    sp.bezier_points.add(len(points)-1)
    for p, co in zip(sp.bezier_points, points):
        p.co = co
        p.handle_left_type = 'AUTO'
        p.handle_right_type = 'AUTO'
    sp.use_cyclic_u = cyclic
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.convert(target='MESH')
    return finish(bpy.context.object, name, mat, bone)


def tapered_tuft(name, base, tip, width, mat, bone='Head'):
    a, b = Vector(base), Vector(tip)
    d = (b-a).normalized()
    tangent = d.cross(Vector((0,1,0))).normalized()
    depth = d.cross(tangent).normalized()
    verts = []
    for t, r in ((0,width), (.38,width*.84), (.72,width*.42)):
        c = a.lerp(b,t)
        for j in range(6):
            ang=j*math.tau/6
            verts.append(c+tangent*math.cos(ang)*r+depth*math.sin(ang)*r*.5)
    verts.append(b)
    faces=[tuple(reversed(range(6)))]
    for ring in range(2):
        for j in range(6):
            faces.append((ring*6+j, ring*6+(j+1)%6,(ring+1)*6+(j+1)%6,(ring+1)*6+j))
    for j in range(6): faces.append((12+j,12+(j+1)%6,18))
    return mesh(name, verts, faces, mat, bone)


def head_surface(x,z, offset=.006):
    v=max(.015, 1-(x/.715)**2-((z-1.755)/.605)**2)
    return -.06-.515*math.sqrt(v)-offset


def forehead_stripe(name, path, widths, mat):
    verts=[]
    for i, ((x,z), width) in enumerate(zip(path,widths)):
        for s in (-1,1):
            xx=x+s*width
            verts.append((xx,head_surface(xx,z,.010),z))
    faces=[(i*2,i*2+1,i*2+3,i*2+2) for i in range(len(path)-1)]
    return mesh(name,verts,faces,mat)


def ear(side, orange, cream, dark):
    s=side
    outline=[(.24,2.18),(.69,2.21),(.65,2.68),(.57,2.63),(.36,2.39)]
    verts=[(s*x,y,z) for y in (-.10,.055) for x,z in outline]
    faces=[tuple(reversed(range(5))),tuple(range(5,10))]
    faces += [(j,(j+1)%5,(j+1)%5+5,j+5) for j in range(5)]
    obj=mesh('Ear.%s.Outer'%s,verts,faces,orange,'Ear.L' if s<0 else 'Ear.R')
    bevel=obj.modifiers.new('Rounded ear edge','BEVEL');bevel.width=.028;bevel.segments=4
    bpy.context.view_layer.objects.active=obj
    bpy.ops.object.modifier_apply(modifier=bevel.name)
    inset=[(s*.355,-.121,2.28),(s*.61,-.121,2.30),(s*.60,-.121,2.56),
           (s*.48,-.121,2.45)]
    ob=mesh('Ear.%s.CreamInterior'%s,inset,[(0,1,2,3)],cream,'Ear.L' if s<0 else 'Ear.R')
    solid=ob.modifiers.new('Inset thickness','SOLIDIFY');solid.thickness=.015
    bpy.context.view_layer.objects.active=ob;bpy.ops.object.modifier_apply(modifier=solid.name)
    for i in range(4):
        tapered_tuft('Ear.%s.InnerFur.%s'%(s,i),(s*(.39+i*.046),-.127,2.29+i*.018),
                     (s*(.37+i*.046),-.135,2.36+i*.018),.023,cream,'Ear.L' if s<0 else 'Ear.R')


def build_cat():
    orange=material('Tabby.HoneyOrange','EBA34D')
    warm=material('Tabby.WarmFur','DA8437')
    stripe=material('Tabby.CopperStripes','D58435')
    cream=material('Tabby.Cream','FFF0C6')
    pink=material('Nose.SoftCoral','D88985',.5)
    ink=material('Face.Ink','282825',.52)
    eye=material('Eyes.GlossyBlack','080F11',.13)
    shine=material('Eyes.Catchlight','FFFFFF',.16)
    black=material('Gear.BlackNylon','171C1C',.84)
    panel=material('Gear.GraphitePanels','2A2F2E',.76)
    edge=material('Gear.Binding','101616',.75)
    seam=material('Gear.Stitching','454A44',.9)
    orange_web=material('Gear.OrangeTabs','E77C41',.64)
    rubber=material('Headset.Rubber','10191B',.64)
    shell=material('Headset.Shell','242E2F',.4)
    blue=material('Headset.BlueIndicator','3E93B2',.3,.1)
    # Mesh fur color is portable vertex color, including the irregular cream chin.
    fur=material('Tabby.FaceVertexCoat','FFFFFF')
    nodes=fur.node_tree.nodes
    vc=nodes.new('ShaderNodeVertexColor');vc.layer_name='Coat'
    fur.node_tree.links.new(vc.outputs['Color'],nodes.get('Principled BSDF').inputs['Base Color'])
    head=ellipsoid('Cat.Head', (0,-.06,1.755),(.715,.515,.605),fur)
    colors=head.data.color_attributes.new(name='Coat',type='FLOAT_COLOR',domain='POINT')
    for v in head.data.vertices:
        p=v.co
        # Deliberately subtle surface variation; the face stays smooth and readable.
        cheek=(1-max(0,min(1,(p.z-1.40)/.17)))*max(0,min(1,(-p.y-.10)/.35))
        limit=1.49-.21*min(1,abs(p.x)/.46)+.012*math.sin(p.x*49)
        mask=max(0,min(1,(limit-p.z)*37+.5))*max(0,min(1,(-p.y-.15)*12))
        co=Vector(rgb('EBA34D')[:3]).lerp(Vector(rgb('FFF0C6')[:3]),mask)
        variation=1+.018*math.sin(p.x*41+p.z*18)*math.sin(p.y*21)
        colors.data[v.index].color=tuple(c*variation for c in co)+(1,)
    # Furry outline; each lock emerges from the cranium instead of a hair system.
    for s in (-1,1):
        for j in range(11):
            a=-.64+j*.142
            x=s*.675*math.cos(a);z=1.75+.57*math.sin(a)
            tapered_tuft('CheekFur.%s.%02d'%(s,j),(x,-.045,z),
                         (x+s*(.055+.012*(j%3)),-.085,z-.045),.042,orange)
        for j in range(4):
            x=s*(.08+j*.085)
            tapered_tuft('CrownFur.%s.%d'%(s,j),(x,-.04,2.30),
                         (x+s*.06,-.035,2.39+.025*(j%2)),.044,orange)
        ear(s,orange,cream,ink)
    for s in (-1,1):
        x=s*.279;z=1.732;y=head_surface(x,z)
        ellipsoid('Eye.%s.CreamRim'%s,(x,y+.016,z),(.153,.040,.182),cream)
        ellipsoid('Eye.%s.Gloss'%s,(x,y-.007,z+.003),(.141,.052,.169),eye)
        ellipsoid('Eye.%s.LargeCatchlight'%s,(x-.043,y-.055,z+.077),(.030,.009,.037),shine,segments=24,rings=16)
        ellipsoid('Eye.%s.SmallCatchlight'%s,(x+.034,y-.060,z-.039),(.012,.006,.014),shine,segments=16,rings=12)
        # Cream muzzle lobes integrate into the painted chin.
        ellipsoid('Muzzle.%s'%s,(s*.115,-.535,1.429),(.175,.095,.124),cream)
        for j in range(3):
            x=s*(.18+j*.028);z=1.443-j*.026
            ellipsoid('MuzzleDot.%s.%d'%(s,j),(x,head_surface(x,z,.045),z),(.008,.006,.008),warm,segments=12,rings=8)
    # Soft inverted triangular nose with a fine dark border.
    for name,y,scale,mat in [('Nose.Outline',-.650,1.0,ink),('Nose.Pink',-.662,.72,pink)]:
        cx=0;cz=1.535
        verts=[(cx+scale*x,y,cz+scale*z) for x,z in [(-.068,.025),(.068,.025),(0,-.058)]]
        ob=mesh(name,verts,[(0,1,2)],mat)
        sol=ob.modifiers.new('Nose depth','SOLIDIFY');sol.thickness=.018
        bpy.context.view_layer.objects.active=ob;bpy.ops.object.modifier_apply(modifier=sol.name)
        bevel=ob.modifiers.new('Soft triangle','BEVEL');bevel.width=.010;bevel.segments=3
        bpy.ops.object.modifier_apply(modifier=bevel.name)
    tube('Mouth.Center',[(0,-.652,1.486),(0,-.642,1.443),(0,-.632,1.414)],.009,ink)
    tube('Mouth.Left',[(0,-.632,1.414),(-.031,-.628,1.384),(-.059,-.617,1.379)],.008,ink,'Jaw')
    tube('Mouth.Right',[(0,-.632,1.414),(.031,-.628,1.384),(.059,-.617,1.379)],.008,ink,'Jaw')
    forehead_stripe('Forehead.Center',[(0,2.295),(-.022,2.24),(-.035,2.16),(-.017,2.07),(0,2.015)],[.028,.055,.045,.033,.001],stripe)
    for s in (-1,1):
        forehead_stripe('Forehead.%s'%s,[(s*.25,2.265),(s*.23,2.20),(s*.18,2.13),(s*.13,2.06)],[.001,.044,.035,.001],stripe)
    ellipsoid('Body.Orange', (0,.12,.72),(.48,.40,.62),orange,'Chest')
    ellipsoid('Body.CreamBib',(0,-.265,.59),(.265,.13,.34),cream,'Chest')
    for s in (-1,1):
        side='L' if s<0 else 'R'
        ellipsoid('Haunch.'+side,(s*.39,.24,.355),(.265,.32,.34),orange,'Hind.'+side)
        ellipsoid('HindPaw.'+side,(s*.43,.10,.115),(.23,.27,.115),cream,'Hind.'+side)
        ellipsoid('Foreleg.'+side,(s*.245,-.23,.37),(.155,.175,.30),orange,'Front.'+side)
        ellipsoid('FrontPaw.'+side,(s*.245,-.30,.115),(.185,.24,.115),cream,'Front.'+side)
        for j in (-1,0,1):
            x=s*.245+j*.084
            tube('Toe.%s.%s'%(side,j),[(x,-.519,.056),(x,-.531,.105),(x,-.504,.153)],.0045,warm,'Front.'+side)
        for j in range(3):
            # Low-profile sculpted stripes on the exposed hips.
            tube('HipStripe.%s.%d'%(side,j),[(s*.55,.04+j*.09,.49),(s*.61,.09+j*.08,.43),(s*.62,.16+j*.07,.37)],.018,stripe,'Hind.'+side)
    build_tail(orange,cream,stripe)
    build_gear(black,panel,edge,seam,orange_web,rubber,shell,blue)


def build_tail(orange,cream,stripe):
    # Swept, full-volume plume with a cream distal half, not a flat cutout.
    control=[Vector(p) for p in [(0,.40,.38),(.27,.54,.28),(.60,.58,.24),(.82,.58,.34),(.97,.54,.54),(1.00,.49,.78),(.94,.45,1.02),(.88,.43,1.12)]]
    radii=[.13,.17,.21,.235,.24,.20,.12,.008]
    verts=[];faces=[];nr=64;ns=32
    for i in range(nr):
        t=i/(nr-1);v=t*(len(control)-1);k=min(len(control)-2,int(v));f=v-k
        p0=control[max(0,k-1)];p1=control[k];p2=control[k+1];p3=control[min(len(control)-1,k+2)]
        c=.5*((2*p1)+(-p0+p2)*f+(2*p0-5*p1+4*p2-p3)*f*f+(-p0+3*p1-3*p2+p3)*f*f*f)
        d=(.5*((-p0+p2)+2*(2*p0-5*p1+4*p2-p3)*f+3*(-p0+3*p1-3*p2+p3)*f*f)).normalized()
        a=(Vector((0,1,0))-d*d.y).normalized();b=d.cross(a).normalized()
        r0=radii[max(0,k-1)];r1=radii[k];r2=radii[k+1];r3=radii[min(len(radii)-1,k+2)]
        radius=max(.007,.5*(2*r1+(-r0+r2)*f+(2*r0-5*r1+4*r2-r3)*f*f+(-r0+3*r1-3*r2+r3)*f*f*f))
        for j in range(ns):
            ang=j*math.tau/ns
            fluff=1+.035*math.sin(ang*7+t*31)+.023*math.sin(ang*11-t*19)
            verts.append(c+(a*math.cos(ang)*.79+b*math.sin(ang))*radius*fluff)
    for i in range(nr-1):
        for j in range(ns):faces.append((i*ns+j,i*ns+(j+1)%ns,(i+1)*ns+(j+1)%ns,(i+1)*ns+j))
    faces += [tuple(reversed(range(ns))),tuple((nr-1)*ns+j for j in range(ns))]
    coat=material('Tabby.TailVertexCoat','FFFFFF')
    node=coat.node_tree.nodes.new('ShaderNodeVertexColor');node.layer_name='Coat'
    coat.node_tree.links.new(node.outputs['Color'],coat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
    tail=mesh('Tail.FluffyPlume',verts,faces,coat,'Tail')
    colors=tail.data.color_attributes.new(name='Coat',type='FLOAT_COLOR',domain='POINT')
    for i,v in enumerate(tail.data.vertices):
        t=(i//ns)/(nr-1);ang=(i%ns)*math.tau/ns
        threshold=.67+.035*math.sin(ang*5)+.019*math.sin(ang*9)
        cream_mask=max(0,min(1,(t-threshold)*45+.5))
        # Cream feathering also follows the back/underside of the plume.
        cream_mask=max(cream_mask,max(0,min(1,(math.cos(ang)-.42)*8))*max(0,min(1,(t-.32)*8)))
        band=math.exp(-((t-.28)/.025)**2)*.55+math.exp(-((t-.45)/.027)**2)*.42
        base=Vector(rgb('EBA34D')[:3]).lerp(Vector(rgb('D58435')[:3]),min(1,band))
        color=base.lerp(Vector(rgb('FFF0C6')[:3]),cream_mask)
        colors.data[i].color=tuple(color)+(1,)
    for j in range(16):
        t=.35+j*.035;v=t*(len(control)-1);k=min(len(control)-2,int(v));f=v-k
        c=control[k].lerp(control[k+1],f);r=radii[k]*(1-f)+radii[k+1]*f
        tip=(c.x+r*.83,c.y+.02,c.z+.075)
        tapered_tuft('Tail.Fur.%02d'%j,(c.x+r*.60,c.y+.035,c.z-.035),tip,.025,cream if t>.70 else orange,'Tail')


def build_gear(black,panel,edge,seam,orange_web,rubber,shell,blue):
    box('Vest.FrontCarrier',(0,-.298,.94),(.92,.18,.48),.095,black)
    box('Vest.BackCarrier',(0,.47,.93),(.94,.18,.53),.09,black)
    for s in (-1,1):
        # Broad shoulder straps connect the vest front and back.
        tube('Vest.Shoulder.%s'%s,[(s*.36,-.30,1.08),(s*.37,-.13,1.23),(s*.37,.21,1.26),(s*.36,.47,1.11)],.092,black,'Chest')
        box('Vest.FrontPlate.%s'%s,(s*.218,-.402,1.015),(.402,.10,.246),.049,panel)
        box('Vest.FrontPlateBinding.%s'%s,(s*.218,-.454,1.015),(.365,.013,.204),.037,edge)
        box('Vest.FrontPlateFace.%s'%s,(s*.218,-.464,1.018),(.344,.018,.181),.035,panel)
        box('Vest.SideStrap.%s'%s,(s*.455,.13,.89),(.13,.58,.20),.038,edge)
        for row,z in enumerate((.99,.73)):
            box('BackPouch.%s.%s'%(s,row),(s*.239,.59,z),(.408,.23,.235),.047,panel)
            box('BackPouchFlap.%s.%s'%(s,row),(s*.239,.724,z+.044),(.36,.022,.125),.025,black)
            tube('BackPouchSeam.%s.%s'%(s,row),[(s*.239-.15,.740,z+.03),(s*.239,.747,z+.013),(s*.239+.15,.740,z+.03)],.005,seam,'Chest')
    box('Vest.LowerPlate',(0,-.366,.724),(.50,.16,.30),.065,edge)
    box('Vest.LowerPlateFace',(0,-.459,.729),(.433,.029,.24),.042,panel)
    tube('Vest.FrontSeam',[(-.18,-.479,.651),(0,-.484,.637),(.18,-.479,.651)],.0055,seam,'Chest')
    for z in (.66,.89,1.14):
        box('Back.OrangeWebbing.%.2f'%z,(0,.588,z),(.16,.027,.035),.012,orange_web)
    tube('Back.OrangeLoop',[(-.08,.54,1.17),(-.073,.56,1.29),(.072,.56,1.29),(.08,.54,1.17)],.019,orange_web,'Chest')
    # Small safety-orange loop at the front matches the drawing.
    tube('Vest.OrangeCarabiner',[(-.365,-.451,1.098),(-.416,-.461,1.055),(-.398,-.47,.994),(-.35,-.46,1.012)],.016,orange_web,'Chest')
    box('Radio.Body',(.576,.32,.965),(.235,.205,.48),.036,black)
    box('Radio.Battery',(.581,.32,.729),(.229,.211,.13),.024,rubber)
    box('Radio.Front',(.704,.32,1.017),(.028,.15,.24),.012,panel)
    tube('Radio.Antenna',[(.60,.37,1.19),(.625,.37,1.43),(.64,.37,1.49)],.019,rubber,'Chest')
    for i in range(4):
        tube('Radio.Grille.%s'%i,[(.723,.27,1.077-i*.032),(.723,.36,1.077-i*.032)],.006,edge,'Chest')
    # Headband runs around the BACK of the head, with one main ear cup.
    tube('Headset.PaddedRearBand',[(.69,-.01,1.99),(.62,.31,2.06),(0,.473,2.075),(-.59,.31,2.06),(-.68,.00,1.99)],.083,rubber)
    tube('Headset.BandInset',[(.67,.04,2.015),(.58,.337,2.10),(0,.486,2.115),(-.58,.337,2.10),(-.67,.04,2.015)],.026,shell)
    ellipsoid('Headset.Cushion',(.684,-.075,1.795),(.13,.235,.295),rubber)
    ellipsoid('Headset.EarCup',(.774,-.075,1.80),(.095,.211,.264),shell)
    ellipsoid('Headset.OuterPad',(.85,-.075,1.80),(.024,.167,.211),rubber)
    tube('Headset.BlueAccent',[(.874,-.160,1.68),(.880,-.180,1.73),(.881,-.180,1.79)],.011,blue)
    tube('Headset.Yoke',[(.76,.063,2.02),(.87,-.03,2.09),(.90,-.19,1.94),(.85,-.264,1.75)],.026,rubber)
    tube('Headset.MicrophoneBoom',[(.79,-.23,1.71),(.64,-.47,1.56),(.46,-.64,1.46),(.24,-.697,1.43)],.026,rubber)
    ellipsoid('Headset.Microphone',(.20,-.708,1.43),(.094,.050,.057),rubber)
    tube('Headset.Cable',[(.72,.10,1.59),(.65,.25,1.39),(.48,.36,1.37),(.52,.36,1.22)],.018,rubber)


def build_rig():
    specs=[('Root',(0,0,.05),(0,0,.25),None),
           ('Chest',(0,.12,.55),(0,.12,1.11),'Root'),
           ('Head',(0,-.06,1.29),(0,-.06,1.98),'Chest'),
           ('Jaw',(0,-.52,1.48),(0,-.64,1.36),'Head'),
           ('Ear.L',(-.46,0,2.24),(-.57,0,2.63),'Head'),
           ('Ear.R',(.46,0,2.24),(.57,0,2.63),'Head'),
           ('Front.L',(-.245,-.23,.70),(-.245,-.23,.11),'Chest'),
           ('Front.R',(.245,-.23,.70),(.245,-.23,.11),'Chest'),
           ('Hind.L',(-.39,.24,.55),(-.43,.10,.12),'Root'),
           ('Hind.R',(.39,.24,.55),(.43,.10,.12),'Root'),
           ('Tail',(0,.40,.38),(.45,.57,.26),'Root')]
    data=bpy.data.armatures.new('TacticalTabby.PosingRig')
    rig=bpy.data.objects.new('TacticalTabby.Rig',data)
    bpy.context.collection.objects.link(rig)
    bpy.context.view_layer.objects.active=rig;rig.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    for name,a,b,parent in specs:
        bone=data.edit_bones.new(name);bone.head=a;bone.tail=b
        if parent:bone.parent=data.edit_bones[parent]
    bpy.ops.object.mode_set(mode='OBJECT')
    rig.show_in_front=True
    for obj in PARTS:
        # All authored coordinates are world-space, so rigid skin weights give
        # clean editable parts and keep accessories attached during posing.
        group=obj.vertex_groups.new(name=WEIGHTS[obj.name])
        group.add(list(range(len(obj.data.vertices))),1,'REPLACE')
        mod=obj.modifiers.new('Pose rig','ARMATURE');mod.object=rig
        obj.parent=rig
    actions={}
    rig.animation_data_create()
    for name,length in [('Idle',120),('LookAround',120),('TailWag',72),('PawWave',96)]:
        action=bpy.data.actions.new(name);rig.animation_data.action=action
        for frame in range(1,length+1,4):
            phase=(frame-1)/length*math.tau
            for bone in rig.pose.bones:
                bone.rotation_mode='XYZ';bone.rotation_euler=(0,0,0);bone.location=(0,0,0);bone.scale=(1,1,1)
            rig.pose.bones['Head'].rotation_euler.y=.018*math.sin(phase)
            rig.pose.bones['Chest'].scale=(1+.006*math.sin(phase),1,1+.007*math.sin(phase))
            if name=='LookAround':
                rig.pose.bones['Head'].rotation_euler.z=.19*math.sin(phase)
                rig.pose.bones['Head'].rotation_euler.x=.045*math.sin(phase*2)
            if name=='TailWag':rig.pose.bones['Tail'].rotation_euler.y=.20*math.sin(phase)
            if name=='PawWave':
                amount=max(0,math.sin(phase/2))
                rig.pose.bones['Front.L'].rotation_euler.x=-.92*amount
                rig.pose.bones['Front.L'].rotation_euler.z=-.22*amount*math.sin(phase*3)
                rig.pose.bones['Head'].rotation_euler.y=-.07*amount
            for bone in rig.pose.bones:
                bone.keyframe_insert(data_path='rotation_euler',frame=frame,group=bone.name)
                bone.keyframe_insert(data_path='scale',frame=frame,group=bone.name)
        # Explicitly close loops at the exact endpoint.
        bpy.context.scene.frame_set(1)
        for bone in rig.pose.bones:
            bone.keyframe_insert(data_path='rotation_euler',frame=length+1,group=bone.name)
            bone.keyframe_insert(data_path='scale',frame=length+1,group=bone.name)
        action.use_fake_user=True
        track=rig.animation_data.nla_tracks.new();track.name=name
        track.strips.new(name,1,action);track.mute=True
        actions[name]=action
    rig.animation_data.action=actions['Idle']
    bpy.context.scene.frame_set(1)
    return rig,actions


def look_at(obj,target):
    obj.rotation_euler=(Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler()


def studio():
    floor_mat=material('Studio.Slate','A7BAB7',.9)
    bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.012))
    floor=bpy.context.object;floor.name='Studio.Ground';floor.data.materials.append(floor_mat)
    world=bpy.context.scene.world;world.use_nodes=True
    world.node_tree.nodes['Background'].inputs['Color'].default_value=(.27,.33,.34,1)
    world.node_tree.nodes['Background'].inputs['Strength'].default_value=.65
    for name,loc,power,size,color in [('Key',(-3,-4,6),450,4,(1,.86,.71)),('Fill',(4,-2,3.6),240,3,(.78,.88,1)),('Rim',(1.3,3,4.8),520,3,(1,.91,.78))]:
        data=bpy.data.lights.new('Studio.'+name,'AREA');data.energy=power;data.size=size;data.color=color
        obj=bpy.data.objects.new(data.name,data);bpy.context.collection.objects.link(obj);obj.location=loc;look_at(obj,(0,0,1.3))
    data=bpy.data.cameras.new('Studio.Camera');camera=bpy.data.objects.new(data.name,data);bpy.context.collection.objects.link(camera)
    camera.data.type='ORTHO';camera.data.ortho_scale=3.35
    scene=bpy.context.scene;scene.camera=camera
    scene.render.engine='BLENDER_EEVEE';scene.eevee.use_gtao=True;scene.eevee.gtao_distance=.18;scene.eevee.gtao_factor=1.25
    scene.eevee.use_soft_shadows=True;scene.eevee.taa_render_samples=96
    scene.render.resolution_x=1100;scene.render.resolution_y=1100;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False
    scene.view_settings.view_transform='Standard';scene.view_settings.look='Medium High Contrast';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    scene.render.fps=30
    return camera


def main():
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    build_cat()
    rig,actions=build_rig()
    camera=studio()
    views={'three-quarter':(4.3,-7,3.35),'front':(0,-8,2.5),'side':(8,0,2.4),'rear':(0,8,2.5),'face-detail':(1.1,-7,2.7)}
    for name,loc in views.items():
        camera.location=loc;look_at(camera,(.10,0,1.36) if name!='face-detail' else (0,-.08,1.88))
        camera.data.ortho_scale=3.28 if name!='face-detail' else 1.98
        bpy.context.scene.render.filepath=os.path.join(PREV,name+'.png')
        bpy.ops.render.render(write_still=True)
    camera.location=views['three-quarter'];look_at(camera,(.1,0,1.36));camera.data.ortho_scale=3.28
    for area in bpy.context.screen.areas:
        if area.type=='VIEW_3D':
            area.spaces.active.region_3d.view_distance=5.3
            area.spaces.active.region_3d.view_location=Vector((0,0,1.35))
            area.spaces.active.region_3d.view_rotation=camera.rotation_euler.to_quaternion()
            area.spaces.active.shading.type='MATERIAL'
    rig.animation_data.action=None
    for track in rig.animation_data.nla_tracks:track.mute=False
    bpy.context.scene.frame_set(1)
    bpy.ops.object.select_all(action='DESELECT')
    for obj in PARTS+[rig]:obj.select_set(True)
    bpy.context.view_layer.objects.active=rig
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT,'tactical-tabby.glb'),export_format='GLB',use_selection=True,export_animations=True,export_nla_strips=True,export_frame_range=False,export_force_sampling=True,export_skins=True,export_def_bones=True,export_yup=True,export_apply=False)
    for track in rig.animation_data.nla_tracks:track.mute=True
    rig.animation_data.action=actions['Idle'];bpy.context.scene.frame_set(1)
    bpy.context.scene.frame_end=120
    reference=os.path.join(OUT,'reference.jpg')
    if os.path.exists(reference):
        drawing=bpy.data.images.load(reference,check_existing=True)
        drawing.name='REFERENCE - user character turnaround'
        drawing.use_fake_user=True
        drawing.pack()
    handoff=bpy.data.texts.new('START HERE - Tactical Tabby')
    handoff.use_fake_user=True
    handoff.write('Original character model based on the user-provided IMG_0664.jpg.\n'
                  'Editable separate mesh parts, portable materials and one posing rig.\n'
                  'Use Pose Mode for head, ears, jaw, forelegs, haunches and tail.\n'
                  'NLA tracks are muted; Idle is the active Action. Select one Action at a time.\n'
                  'Preview motions: Idle, LookAround, TailWag, PawWave.\n'
                  'This seated art candidate is not the active Mega Chonk cat or a drop-in animation replacement.\n'
                  'The supplied turnaround is packed in the Images datablock.\n')
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'tactical-tabby.blend'))
    # Re-import into this disposable process after saving the editable scene.
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    for a in list(bpy.data.actions):bpy.data.actions.remove(a)
    bpy.ops.import_scene.gltf(filepath=os.path.join(OUT,'tactical-tabby.glb'))
    meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
    rigs=[o for o in bpy.context.scene.objects if o.type=='ARMATURE']
    triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in meshes)
    clips=sorted(a.name for a in bpy.data.actions)
    report={'blender':bpy.app.version_string,'meshes':len(meshes),'triangles':triangles,'armatures':len(rigs),'skinnedMeshes':sum(any(m.type=='ARMATURE' for m in o.modifiers) for o in meshes),'clips':clips,'sourceReference':'User supplied IMG_0664.jpg front / side / rear drawing','status':'Separate seated artist candidate; not integrated into gameplay'}
    assert len(rigs)==1 and len(meshes)>100
    assert all(any(name in clip for clip in clips) for name in actions)
    with open(os.path.join(OUT,'verification.json'),'w') as f:json.dump(report,f,indent=2)
    print('TACTICAL_TABBY_VERIFIED',json.dumps(report),flush=True)


if __name__=='__main__':main()
