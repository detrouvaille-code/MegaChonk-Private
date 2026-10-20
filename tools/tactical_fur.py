"""Groomed, skinned kitten coat for the original Tactical Tabby.

The generated alpha atlas is a bitmap art asset. This module authors the UVs,
coat colors, directional surface maps and lightweight curved fur geometry.
Everything exported is standard glTF PBR; no Blender hair system is required.
"""
import bpy
import math
import os
import random
import bisect
import numpy as np
from mathutils import Vector

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEXTURES = os.path.join(ROOT, 'assets', 'models', 'textures', 'tactical-tabby')


def clamp(x):
    return max(0., min(1., x))


def smooth(a, b, x):
    t = clamp((x-a)/(b-a))
    return t*t*(3-2*t)


def head_color(p, rgb):
    orange = Vector(rgb('EDAA62')[:3])
    cream = Vector(rgb('FFF4D9')[:3])
    copper = Vector(rgb('CA7B36')[:3])
    # A soft cream butterfly muzzle/chin with irregular feathered boundaries.
    boundary = .575+.037*math.exp(-((abs(p.x)-.045)/.075)**2)
    boundary += .002*math.sin(p.x*450.)*math.sin(p.z*290.)
    muzzle = (1-smooth(boundary-.010, boundary+.009, p.z))*(1-smooth(-.51, -.44, p.y))
    color = orange.lerp(cream, muzzle)
    # Three tapered copper forehead marks, continuous across skin and fur.
    forehead = smooth(.698, .735, p.z)*(1-smooth(-.48, -.395, p.y))
    taper = smooth(.697, .756, p.z)*(1-smooth(.814, .838, p.z))
    x = abs(p.x)
    center = math.exp(-((p.x+.004*math.sin(p.z*65.))/(.009+.003*taper))**2)
    branch_x = .035 + (p.z-.715)*.46
    branches = math.exp(-((x-branch_x)/(.006+.006*taper))**2)
    stripe = clamp((center+branches)*forehead*taper*.83)
    color = color.lerp(copper, stripe)
    variation = 1.+.035*math.sin(p.x*130.+p.z*71.)*math.sin(p.y*117.-p.z*33.)
    return tuple(c*variation for c in color)+(1.,)


def image_from_array(name, array, noncolor=False):
    height, width = array.shape[:2]
    image = bpy.data.images.new(name, width=width, height=height, alpha=True)
    if noncolor:
        image.colorspace_settings.name = 'Non-Color'
    image.pixels.foreach_set(array.astype(np.float32).ravel())
    image.filepath_raw = os.path.join(TEXTURES, name+'.png')
    image.file_format = 'PNG'
    image.save()
    image.pack()
    return image


def surface_maps():
    """Load the generated undercoat and author fine tangent-space relief."""
    os.makedirs(TEXTURES, exist_ok=True)
    n = 512
    rng = np.random.default_rng(1910664)
    height = np.zeros((n, n), dtype=np.float32)
    # Tapered strokes wrap at the boundaries, so UV repetition has no seam.
    for _ in range(2600):
        x0, y0 = rng.uniform(0, n, 2)
        length = rng.uniform(10., 65.)
        width = rng.uniform(.35, .85)
        amp = rng.uniform(.35, 1.)
        bend = rng.uniform(-4., 4.)
        iy = np.arange(math.floor(y0), math.ceil(y0+length))
        t = (iy-y0)/length
        cx = x0+bend*np.sin(t*math.pi*.65)
        ix = np.arange(math.floor(x0-abs(bend)-3), math.ceil(x0+abs(bend)+3))
        stroke = np.exp(-((ix[None,:]-cx[:,None])/width)**2)
        stroke *= (np.sin(np.clip(t, 0, 1)*math.pi)**.35*amp)[:,None]
        height[np.ix_(iy%n, ix%n)] += stroke
    height /= max(float(np.percentile(height, 98)), .01)
    height = np.clip(height, 0, 1.3)
    dx = (np.roll(height,-1,1)-np.roll(height,1,1))*.13
    dy = (np.roll(height,-1,0)-np.roll(height,1,0))*.13
    normal = np.stack((-dx,-dy,np.ones_like(dx)),axis=-1)
    normal /= np.linalg.norm(normal,axis=-1,keepdims=True)
    normal_map = np.ones((n,n,4),dtype=np.float32)
    normal_map[:,:,:3] = normal*.5+.5
    normal_image=image_from_array('kitten-fur-normal',normal_map,True)
    undercoat=bpy.data.images.load(os.path.join(TEXTURES,'kitten-undercoat.png'),check_existing=True)
    undercoat.name='Kitten soft undercoat - generated art';undercoat.pack()
    return undercoat,normal_image


def material(name, image, normal=None, alpha=False):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    bsdf = nodes.get('Principled BSDF')
    bsdf.inputs['Roughness'].default_value = .91
    bsdf.inputs['Specular'].default_value = .24
    bsdf.inputs['Sheen'].default_value = .32
    tex = nodes.new('ShaderNodeTexImage');tex.image=image
    colors = nodes.new('ShaderNodeVertexColor');colors.layer_name='Coat'
    multiply = nodes.new('ShaderNodeMixRGB');multiply.blend_type='MULTIPLY';multiply.inputs[0].default_value=1.
    links.new(tex.outputs['Color'],multiply.inputs[1]);links.new(colors.outputs['Color'],multiply.inputs[2])
    links.new(multiply.outputs[0],bsdf.inputs['Base Color'])
    if normal:
        nm = nodes.new('ShaderNodeTexImage');nm.image=normal
        strength = nodes.new('ShaderNodeNormalMap');strength.inputs['Strength'].default_value=.22
        links.new(nm.outputs['Color'],strength.inputs['Color']);links.new(strength.outputs['Normal'],bsdf.inputs['Normal'])
    if alpha:
        links.new(tex.outputs['Alpha'],bsdf.inputs['Alpha'])
        mat.blend_method='CLIP';mat.alpha_threshold=.40
        mat.use_backface_culling=False
        mat.use_screen_refraction=False
    return mat


def set_uv(obj):
    """Spherical, cylindrical or swept UVs matched to each coat surface."""
    layer = obj.data.uv_layers.active or obj.data.uv_layers.new(name='FurUV')
    name = obj.name
    coords = []
    for vertex in obj.data.vertices:
        p = vertex.co
        if name=='TacticalTabby.Cat.Head':
            q=p-Vector((0,-.39,.65))
            u=math.atan2(q.x,-q.y)/math.tau+.5
            v=.5+math.asin(max(-1.,min(1.,q.z/.180)))/math.pi
            coords.append((u*3.,v*2.))
        elif name=='TacticalTabby.Tail.FluffyPlume':
            coords.append(((vertex.index%64)/64.*1.5,(vertex.index//64)/111.*3.))
        elif '.Leg.' in name:
            coords.append(((vertex.index%24)/24.,(vertex.index//24)/41.*2.))
        elif '.Paw.' in name:
            coords.append((p.x*25.,p.y*25.))
        else:
            coords.append((p.x*8.,p.z*8.))
    for poly in obj.data.polygons:
        values=[coords[obj.data.loops[i].vertex_index] for i in poly.loop_indices]
        # Repair the azimuth seam before interpolating the surface map.
        period=3. if name=='TacticalTabby.Cat.Head' else 1.5 if name=='TacticalTabby.Tail.FluffyPlume' else 1. if '.Leg.' in name else 0.
        if period and max(u for u,v in values)-min(u for u,v in values)>period*.65:
            values=[(u+period if u<period*.4 else u,v) for u,v in values]
        for loop_index,uv in zip(poly.loop_indices,values):layer.data[loop_index].uv=uv


def remodel(parts,assign,art):
    """Refine the exposed anatomy while preserving the gameplay skeleton."""
    for obj in list(parts):
        if any(token in obj.name for token in ('.Forehead.','.CheekFur.','.Tail.Fur.')):
            parts.remove(obj);assign.pop(obj.name,None);bpy.data.objects.remove(obj,do_unlink=True)
    head = next(obj for obj in parts if obj.name=='TacticalTabby.Cat.Head')
    colors=head.data.color_attributes['Coat']
    for vertex in head.data.vertices:
        p=vertex.co
        # Rounder lower cheeks and a soft, non-spherical brow silhouette.
        cheek=math.exp(-((p.z-.600)/.052)**2)*smooth(.09,.17,abs(p.x))
        p.x+=math.copysign(.009*cheek,p.x)
        p.z+=.002*math.sin(p.x*42.)*smooth(.77,.82,p.z)
        front=1-smooth(-.52,-.46,p.y)
        p.y-=.008*math.exp(-((abs(p.x)-.026)/.047)**2-((p.z-.576)/.027)**2)*front
        colors.data[vertex.index].color=head_color(p,art.rgb)
    head.data.update()
    for obj in parts:
        if '.Eye.' in obj.name:
            side=-1 if '.-1.' in obj.name else 1
            for vertex in obj.data.vertices:
                vertex.co.x=side*.0774+(vertex.co.x-side*.0774)*1.06
                vertex.co.z=.6375+(vertex.co.z-.6375)*.90
            obj.data.update()
        elif any(token in obj.name for token in ('.Nose.','.Mouth.','.MuzzleDot.')):
            for vertex in obj.data.vertices:vertex.co.y-=.008
            obj.data.update()
    for mat in bpy.data.materials:
        if mat.name.startswith('Gear.'):
            node=mat.node_tree.nodes.get('Principled BSDF')
            node.inputs['Roughness'].default_value=.89
            node.inputs['Specular'].default_value=.21
    # Fine white whiskers, attached to the same head/jaw system as the face.
    cream=bpy.data.materials['TacticalTabby.Fur.Cream']
    for side in (-1,1):
        for i in range(3):
            z=.574-i*.006
            obj=art.tube('TacticalTabby.Whisker.%s.%d'%(side,i),[(side*.044,-.576,z),(side*.088,-.594,z+.002),(side*.153,-.594,z+(i-1)*.018)],.00025,cream,'Head')
            parts.append(obj);assign[obj.name]='Head'


def groom(parts,assign,art,add):
    diffuse, normal = surface_maps()
    skin = material('TacticalTabby.Fur.GroomedSurface',diffuse,normal)
    atlas=bpy.data.images.load(os.path.join(TEXTURES,'kitten-fur-atlas.png'),check_existing=True)
    atlas.name='Kitten fur card atlas - generated art';atlas.pack()
    strands=material('TacticalTabby.Fur.GroomedStrands',atlas,alpha=True)
    randomizer=random.Random(1910664)
    plans=[]
    for obj in list(parts):
        if not any(m and m.name.startswith('TacticalTabby.Fur.') for m in obj.data.materials):continue
        if '.Whisker.' in obj.name:continue
        existing_colors=obj.data.color_attributes.get('Coat')
        colors=existing_colors or obj.data.color_attributes.new(name='Coat',type='FLOAT_COLOR',domain='POINT')
        vertex_materials={}
        if not existing_colors and '.Ear.' in obj.name:
            for polygon in obj.data.polygons:
                for index in polygon.vertices:
                    vertex_materials.setdefault(index,polygon.material_index)
        for vertex in obj.data.vertices:
            if not existing_colors:
                poly_material=obj.data.materials[0]
                # Ear bowls have separate orange and ivory material regions.
                if '.Ear.' in obj.name:
                    adjacent=vertex_materials.get(vertex.index,0)
                    poly_material=obj.data.materials[adjacent]
                colors.data[vertex.index].color=poly_material.diffuse_color
        obj.data.materials.clear();obj.data.materials.append(skin)
        for face in obj.data.polygons:face.material_index=0
        set_uv(obj)
        name=obj.name
        if name=='TacticalTabby.Cat.Head':plans.append((obj,16000,.012,.00065))
        elif name=='TacticalTabby.Body':plans.append((obj,5000,.016,.00070))
        elif name=='TacticalTabby.Tail.FluffyPlume':plans.append((obj,5500,.027,.00080))
        elif '.Leg.' in name:plans.append((obj,1000,.010,.00060))
        elif '.Paw.' in name:plans.append((obj,220,.005,.00050))
        elif '.Ear.' in name:plans.append((obj,750,.016,.00050))
    for obj,count,length,width in plans:
        print('GROOMING',obj.name,count,flush=True)
        mesh=obj.data;mesh.calc_loop_triangles();mesh.update()
        triangles=list(mesh.loop_triangles)
        cumulative=[];area=0.
        for tri in triangles:
            area+=tri.area;cumulative.append(area)
        vertices=[];faces=[];uvs=[];coats=[];normals=[]
        for _ in range(count):
            tri=triangles[min(len(triangles)-1,bisect.bisect_left(cumulative,randomizer.random()*area))]
            a,b,c=[mesh.vertices[i] for i in tri.vertices]
            r1=math.sqrt(randomizer.random());r2=randomizer.random()
            weights=(1-r1,r1*(1-r2),r1*r2)
            p=sum((v.co*w for v,w in zip((a,b,c),weights)),Vector())
            n=sum((v.normal*w for v,w in zip((a,b,c),weights)),Vector()).normalized()
            if obj.name=='TacticalTabby.Cat.Head':
                # Leave eyes, nose and headset earcup unobstructed.
                if p.y<-.465 and any(((p.x-x)/.048)**2+((p.z-.6375)/.057)**2<1. for x in (-.0774,.0774)):continue
                if p.y<-.51 and abs(p.x)<.030 and .552<p.z<.618:continue
                if p.x>.182 and -.455<p.y<-.305 and .60<p.z<.755:continue
                direction=Vector((p.x*3.,.06,(p.z-.625)*2.))
                fiber_length=length*(.70+1.35*smooth(.11,.18,abs(p.x)))
                color=head_color(p,art.rgb)
            elif obj.name=='TacticalTabby.Body':
                # The vest covers the upper spine; avoid filling its surface.
                if p.z>.39 and p.y<.22:continue
                if p.z<.27:continue
                direction=Vector((p.x*.7,.5,-.3));fiber_length=length
                color=tuple(sum(mesh.color_attributes['Coat'].data[v.index].color[k]*w for v,w in zip((a,b,c),weights)) for k in range(4))
            else:
                if p.z<.046:continue
                direction=Vector((p.x*.4,.3,-.15 if p.z>.15 else .4));fiber_length=length
                color=tuple(sum(mesh.color_attributes['Coat'].data[v.index].color[k]*w for v,w in zip((a,b,c),weights)) for k in range(4))
            tangent=direction-n*direction.dot(n)
            if tangent.length<.01:tangent=n.cross(Vector((1,0,0)))
            tangent.normalize();across=tangent.cross(n).normalized()
            fiber_length*=randomizer.uniform(.70,1.25)
            card_width=width*randomizer.uniform(.75,1.20)
            tile=randomizer.randrange(16);column=tile%4;row=3-tile//4
            strand_u=.50+randomizer.uniform(-.065,.065)
            base=len(vertices)
            for segment in range(3):
                t=segment/2.
                center=p+n*(.00015+fiber_length*.30*t*t)+tangent*fiber_length*.92*t
                for side in (-1,1):
                    point=center+across*side*card_width*.5*(1-.94*t)
                    vertices.append(point);coats.append(color);normals.append(n)
                    uvs.append(((column+strand_u+side*.003)/4.,(row+.10+t*.77)/4.))
            for segment in range(2):faces.append((base+segment*2,base+segment*2+1,base+segment*2+3,base+segment*2+2))
        fur=art.mesh(obj.name+'.Groom',vertices,faces,strands,assign[obj.name])
        colors=fur.data.color_attributes.new(name='Coat',type='FLOAT_COLOR',domain='POINT')
        for i,color in enumerate(coats):colors.data[i].color=color
        uv=fur.data.uv_layers.new(name='FurAtlasUV')
        for loop in fur.data.loops:uv.data[loop.index].uv=uvs[loop.vertex_index]
        fur.data.use_auto_smooth=True
        fur.data.normals_split_custom_set_from_vertices(normals)
        add(fur,assign[obj.name])
    return {'surfaceTexture':diffuse.name,'normalTexture':normal.name,'atlas':atlas.name,'groomedSurfaces':len(plans)}
