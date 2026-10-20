"""Build the original tactical-tabby character's seven-clip gameplay rig.

Run in a separate Blender --background --factory-startup process. Neither
artist candidate nor canonical Turkish Van files are loaded or overwritten.
Uses shared project IK/clip-authoring helpers, not the original cat's mesh.
"""
import bpy
import os
import sys
import math
import json
import random
import struct
import hashlib
from mathutils import Vector, Matrix

sys.path.insert(0, os.path.dirname(__file__))
import build_tactical_tabby as art
import generate_stray_style_cat as motion
import tactical_fur

ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
MODEL=os.path.join(ROOT,'assets','models')
PREVIEW=os.path.join(MODEL,'tactical-tabby-game-previews')
os.makedirs(PREVIEW,exist_ok=True)
PARTS=[]
ASSIGN={}
TAIL=[Vector((x*.32,.48+(y-.40)*.32,.40+(z-.38)*.32)) for x,y,z in
      [(0,.40,.38),(.27,.54,.28),(.60,.58,.24),(.82,.58,.34),(.97,.54,.54),(1,.49,.78),(.94,.45,1.02),(.88,.43,1.12)]]


def clamp(v):return max(0,min(1,v))
def smooth(a,b,v):
    t=clamp((v-a)/(b-a));return t*t*(3-2*t)


def tail_point(t):
    v=t*(len(TAIL)-1);k=min(len(TAIL)-2,int(v));f=v-k
    return TAIL[k].lerp(TAIL[k+1],f)


def add(obj,kind):
    PARTS.append(obj);ASSIGN[obj.name]=kind
    return obj


def original_parts():
    art.build_cat()
    for obj in list(art.PARTS):
        name=obj.name;bone=art.WEIGHTS[name]
        if name.startswith(('Body.','Haunch.','HindPaw.','Foreleg.','FrontPaw.','Toe.','HipStripe.','Vest.Front','Vest.Lower')) or name=='Headset.Cable':
            bpy.data.objects.remove(obj,do_unlink=True);continue
        for v in obj.data.vertices:
            p=v.co.copy()
            if bone in ('Head','Jaw','Ear.L','Ear.R'):
                p=(p-Vector((0,-.06,1.755)))*.29+Vector((0,-.39,.65))
            elif bone=='Tail':
                p=(p-Vector((0,.40,.38)))*.32+Vector((0,.48,.40))
            elif name.startswith('Radio.'):
                p=(p-Vector((.576,.32,.965)))*.30+Vector((.205,.02,.42))
            else:
                p=Vector((p.x*.34,-.08-(p.z-.95)*.34,.43+(p.y-.12)*.34))
            v.co=p
        obj.data.update()
        for mat in obj.data.materials:
            if mat.name.startswith('Tabby.'):
                mat.name='TacticalTabby.Fur.'+mat.name.removeprefix('Tabby.')
                mat.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.92
        obj.name='TacticalTabby.'+name
        kind=bone
        if name.startswith('Eye.'):
            kind='Eyelid.L' if name.startswith('Eye.-1.') else 'Eyelid.R'
        if name.startswith('Tail.'):kind='tail'
        add(obj,kind)


def coat_material():
    mat=art.material('TacticalTabby.Fur.Coat','FFFFFF',.94)
    node=mat.node_tree.nodes.new('ShaderNodeVertexColor');node.layer_name='Coat'
    mat.node_tree.links.new(node.outputs['Color'],mat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
    return mat


def paint(obj,center=(0,0,0),cream_feet=False):
    coat=obj.data.color_attributes.new(name='Coat',type='FLOAT_COLOR',domain='POINT')
    for vertex in obj.data.vertices:
        p=vertex.co
        color=Vector(art.rgb('E8A052')[:3])
        band=(math.exp(-((p.y-.01)/.022)**2)+math.exp(-((p.y-.15)/.025)**2)+math.exp(-((p.y-.29)/.025)**2))
        side=smooth(.08,.14,abs(p.x))*(1-smooth(.59,.66,p.z))
        color=color.lerp(Vector(art.rgb('C77D39')[:3]),clamp(band*side*.62))
        cream=(1-smooth(.105,.145,p.z)) if cream_feet else (1-smooth(.29,.37,p.z))*.7
        color=color.lerp(Vector(art.rgb('FFF0CB')[:3]),cream)
        coat.data[vertex.index].color=tuple(color)+(1,)


def body_and_legs():
    fur=coat_material()
    body=art.ellipsoid('TacticalTabby.Body',(0,.055,.38),(.195,.355,.178),fur,'Chest',segments=72,rings=48)
    paint(body);add(body,'body')
    for side,s in (('L',-1),('R',1)):
        for front in (True,False):
            leg=('Front.' if front else 'Hind.')+side
            points=[Vector(p) for p in ([(s*.09,-.175,.390),(s*.09,-.160,.245),(s*.09,-.205,.075)] if front else [(s*.12,.34,.39),(s*.115,.445,.20),(s*.10,.365,.08)])]
            shape_points=[points[0]+Vector((0,.035 if front else -.07,.055)),points[1],points[2]]
            verts=[];faces=[];count=42;sides=24
            for i in range(count):
                t=i/(count-1);v=t*2;k=min(1,int(v));f=v-k
                p0=shape_points[max(0,k-1)];p1=shape_points[k];p2=shape_points[k+1];p3=shape_points[min(2,k+2)]
                p=.5*(2*p1+(-p0+p2)*f+(2*p0-5*p1+4*p2-p3)*f*f+(-p0+3*p1-3*p2+p3)*f*f*f)
                tangent=((-p0+p2)+2*(2*p0-5*p1+4*p2-p3)*f+3*(-p0+3*p1-3*p2+p3)*f*f).normalized()
                a=Vector((1,0,0));b=tangent.cross(a).normalized()
                if front:r=.042*(1-t)+.035*t+.029*math.sin(t*math.pi)**.8
                else:r=.035*(1-t)+.036*t+.062*math.sin(t*math.pi)**.8
                for j in range(sides):
                    angle=j*math.tau/sides
                    verts.append(p+a*math.cos(angle)*r+b*math.sin(angle)*r*(1.04 if front else 1.12))
            for i in range(count-1):
                for j in range(sides):faces.append((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j))
            faces += [tuple(reversed(range(sides))),tuple((count-1)*sides+j for j in range(sides))]
            obj=art.mesh('TacticalTabby.Leg.'+leg,verts,faces,fur,leg+'.Upper')
            paint(obj,cream_feet=True);add(obj,('leg',leg,points))
            ankle=points[-1]
            center=(ankle.x,ankle.y-.026, .052 if front else .057)
            paw=art.ellipsoid('TacticalTabby.Paw.'+leg,center,(.057,.079,.049),bpy.data.materials.get('TacticalTabby.Fur.Cream'),leg+'.Paw',segments=40,rings=24)
            add(paw,leg+'.Paw')
            for j in (-1,1):
                x=ankle.x+j*.019;y=center[1]-.074
                groove=art.tube('TacticalTabby.Toe.'+leg+str(j),[(x,y,.035),(x,y-.003,.055),(x,y+.007,.071)],.0009,bpy.data.materials.get('Face.Ink'),leg+'.Paw')
                add(groove,leg+'.Paw')
    cable=art.tube('TacticalTabby.Headset.FlexCable',[(.213,-.36,.603),(.216,-.24,.50),(.207,-.06,.51),(.205,.02,.49)],.005,bpy.data.materials.get('Headset.Rubber'),'Chest')
    add(cable,'cable')
    tongue=art.ellipsoid('TacticalTabby.Tongue',(0,-.572,.558),(.014,.024,.004),bpy.data.materials.get('Nose.SoftCoral'),'Tongue',segments=24,rings=16)
    add(tongue,'Tongue')
    black=bpy.data.materials['Gear.BlackNylon'];panel=bpy.data.materials['Gear.GraphitePanels'];seam=bpy.data.materials['Gear.Stitching']
    add(art.box('TacticalTabby.Vest.FrontBib',(0,-.286,.389),(.345,.075,.195),.045,black),'Chest')
    for s in (-1,1):
        add(art.box('TacticalTabby.Vest.ChestPouch.%s'%s,(s*.080,-.332,.417),(.148,.052,.094),.028,panel),'Chest')
        add(art.tube('TacticalTabby.Vest.Seam.%s'%s,[(s*.080-.05,-.356,.396),(s*.080,-.36,.390),(s*.080+.05,-.356,.396)],.0012,seam,'Chest'),'Chest')
    add(art.box('TacticalTabby.Vest.LowerPouch',(0,-.318,.299),(.181,.068,.138),.035,panel),'Chest')


def micro_fur():
    # Short opaque mesh fibers provide a soft silhouette without hair particles
    # or a transparency-heavy shell shader. Meshes keep the same skin weights.
    random.seed(664)
    for label,center,radii,n,bone in [('Head',(0,-.39,.65),(.209,.151,.176),900,'Head'),('Body',(0,.055,.38),(.196,.356,.179),350,'body')]:
        verts=[];faces=[];colors=[]
        for i in range(n):
            u=random.uniform(-1,1);a=random.uniform(0,math.tau);r=math.sqrt(1-u*u)
            normal=Vector((r*math.cos(a),r*math.sin(a),u));p=Vector(center)+Vector(tuple(normal[k]*radii[k] for k in range(3)))
            # Keep fibers out of the face, paw support and tactical equipment.
            if label=='Head' and normal.y<-.43 and abs(normal.x)<.75 and normal.z<.65:continue
            if label=='Body' and p.z<.24:continue
            tangent=normal.cross(Vector((0,0,1)))
            if tangent.length<.1:tangent=Vector((1,0,0))
            tangent.normalize();bitangent=normal.cross(tangent).normalized()
            length=random.uniform(.003,.006);width=random.uniform(.00035,.00065)
            base=len(verts)
            for offset,scale in ((0,1),(.6,.6)):
                c=p+normal*length*offset
                for j in range(4):
                    angle=j*math.tau/4;verts.append(c+width*scale*(tangent*math.cos(angle)+bitangent*math.sin(angle)))
            verts.append(p+normal*length+Vector((0,.001,-.002)))
            for j in range(4):
                faces.append((base+j,base+(j+1)%4,base+4+(j+1)%4,base+4+j))
                faces.append((base+4+j,base+4+(j+1)%4,base+8))
        obj=art.mesh('TacticalTabby.'+label+'Fluff',verts,faces,bpy.data.materials['TacticalTabby.Fur.Coat'],bone)
        paint(obj);add(obj,bone)


def make_rig():
    specs=[]
    for name,a,b,parent,deform in motion.BONE_SPECS:
        if name.startswith('Tail.'):continue
        a=Vector(a);b=Vector(b)
        if name in ('Pelvis','Spine','Chest','Scapula.L','Scapula.R'):
            a.z-=.10;b.z-=.10
        if name=='Neck':a.z-=.10;b.z-=.05
        if name.startswith('Front.') and name.endswith('Upper'):a.z-=.10;b.z-=.10
        if name.startswith('Front.') and name.endswith('Lower'):a.z-=.10
        if name.startswith('Hind.') and name.endswith('Upper'):a.z-=.10;b.z-=.05
        if name.startswith('Hind.') and name.endswith('Lower'):a.z-=.05
        if name=='Head':a=(0,-.39,.61);b=(0,-.45,.71)
        if name=='Jaw':a=(0,-.48,.576);b=(0,-.56,.555)
        if name=='Tongue':a=(0,-.56,.558);b=(0,-.59,.557)
        if name.startswith('Ear.'):
            s=-1 if name.endswith('L') else 1;a=(s*.14,-.39,.785);b=(s*.18,-.39,.905)
        if name.startswith('Eyelid.'):
            s=-1 if name.endswith('L') else 1;a=(s*.0774,-.53,.6375);b=(s*.0774,-.53,.6775)
        specs.append((name,a,b,parent,deform))
    for i in range(6):specs.append(('Tail.%d'%(i+1),tail_point(i/6),tail_point((i+1)/6),'Pelvis' if i==0 else 'Tail.%d'%i,True))
    data=bpy.data.armatures.new('TacticalTabby.GameRig');rig=bpy.data.objects.new('TacticalTabby.GameRig',data);bpy.context.collection.objects.link(rig)
    bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
    for name,a,b,parent,deform in specs:
        bone=data.edit_bones.new(name);bone.head=a;bone.tail=b;bone.use_deform=True
        if parent:bone.parent=data.edit_bones[parent]
    bpy.ops.object.mode_set(mode='OBJECT');rig.show_in_front=True
    def group(obj,name,index,weight):
        if weight<1e-6:return
        vg=obj.vertex_groups.get(name) or obj.vertex_groups.new(name=name);vg.add([index],weight,'REPLACE')
    def distance(p,a,b):
        d=b-a;t=clamp((p-a).dot(d)/d.length_squared)
        return (p-a-d*t).length
    for obj in PARTS:
        kind=ASSIGN[obj.name]
        for v in obj.data.vertices:
            p=v.co
            if kind=='body':
                pelvis=smooth(.04,.29,p.y);chest=1-smooth(-.20,.09,p.y);spine=max(0,1-pelvis-chest)
                total=pelvis+chest+spine
                for name,w in [('Pelvis',pelvis),('Chest',chest),('Spine',spine)]:group(obj,name,v.index,w/total)
            elif kind=='tail':
                ranked=sorted((distance(p,Vector(a),Vector(b)),name) for name,a,b,_,_ in specs if name.startswith('Tail.'))[:2]
                weights=[1/(d+.008)**2 for d,_ in ranked];total=sum(weights)
                for (_,name),w in zip(ranked,weights):group(obj,name,v.index,w/total)
            elif isinstance(kind,tuple):
                _,leg,points=kind;da=distance(p,points[0],points[1]);db=distance(p,points[1],points[2]);wa=1/(da+.018)**3;wb=1/(db+.018)**3
                group(obj,leg+'.Upper',v.index,wa/(wa+wb));group(obj,leg+'.Lower',v.index,wb/(wa+wb))
            elif kind=='cable':
                head=1-smooth(-.33,-.18,p.y);group(obj,'Head',v.index,head);group(obj,'Chest',v.index,1-head)
            elif obj.name=='TacticalTabby.Cat.Head':
                jaw=(1-smooth(.558,.585,p.z))*(1-smooth(-.52,-.48,p.y))
                group(obj,'Jaw',v.index,jaw);group(obj,'Head',v.index,1-jaw)
            else:group(obj,kind,v.index,1)
        mod=obj.modifiers.new('Game skeletal deformation','ARMATURE');mod.object=rig;obj.parent=rig
        if kind=='body' or kind=='Chest' and not obj.name.startswith('TacticalTabby.Headset'):
            obj.shape_key_add(name='Basis');key=obj.shape_key_add(name='Chonk')
            for v in key.data:
                p=v.co;mask=smooth(.16,.30,p.z)*(1-smooth(.56,.69,p.z))*math.exp(-((p.y-.04)/.38)**4)
                p.x+=p.x*.55*mask;p.z+=(p.z-.41)*.12*mask;p.y+=p.y*.08*mask
    return rig


def game_key_pose(armature,frame,rotations=None,locations=None,scales=None,root=(0,0,0),feet=None):
    rotations=rotations or {};locations=locations or {};scales={'Tongue':(.001,.001,.001),**(scales or {})}
    action=armature.animation_data.action.name
    root=Vector(root)
    if action in ('Sit','Groom'):root.z*=.52
    for bone in armature.pose.bones:
        bone.rotation_mode='XYZ';bone.rotation_euler=rotations.get(bone.name,(0,0,0));bone.location=locations.get(bone.name,(0,0,0));bone.scale=scales.get(bone.name,(1,1,1))
        if bone.name=='Root':bone.location=bone.bone.matrix_local.to_3x3().inverted()@root
    bpy.context.view_layer.update()
    if action in ('Sit','Groom'):
        # Keep fore shoulders within the legs' reach while the hindquarters sit.
        amount=clamp(-root.z/.1274)
        shoulder=armature.pose.bones['Front.R.Upper'].head.z
        chest=armature.pose.bones['Chest'];matrix=chest.matrix.copy()
        matrix.translation.z-=max(0,shoulder-.35)*amount
        chest.matrix=matrix;bpy.context.view_layer.update()
    if feet:
        for leg,target in feet.items():
            target=Vector(target)
            if action=='Groom' and leg=='Front.L':target.z-=.21
            motion.solve_leg(armature,leg,target,rotations.get(leg+'.Paw',(0,0,0))[0])
    for bone in armature.pose.bones:
        for path in ('rotation_euler','location','scale'):bone.keyframe_insert(data_path=path,frame=frame,group=bone.name)


def main():
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    print('Building character surfaces',flush=True)
    original_parts();body_and_legs()
    tactical_fur.remodel(PARTS,ASSIGN,art)
    coat_report=tactical_fur.groom(PARTS,ASSIGN,art,add)
    print('Skinning groomed character',flush=True)
    rig=make_rig()
    if '--coat-preview' in sys.argv:
        camera=art.studio();scene=bpy.context.scene
        scene.render.resolution_x=scene.render.resolution_y=850
        for light in scene.objects:
            if light.type=='LIGHT':light.location*=.4;light.data.energy*=.16;light.data.size*=.4;art.look_at(light,(0,0,.45))
        camera.location=(.20,-2.2,.75);art.look_at(camera,(0,-.39,.68));camera.data.ortho_scale=.58
        scene.render.filepath=os.path.join(PREVIEW,'coat-draft.png');bpy.ops.render.render(write_still=True)
        return
    motion.key_pose=game_key_pose
    print('Authoring seven actions',flush=True)
    # IK authors only bone transforms. Avoid needlessly deforming the entire
    # groom on every intermediate solver update; restore it before inspection.
    geometry_collection=bpy.data.collections.new('Character geometry')
    bpy.context.scene.collection.children.link(geometry_collection)
    for obj in PARTS:
        for collection in list(obj.users_collection):collection.objects.unlink(obj)
        geometry_collection.objects.link(obj)
    geometry_layer=bpy.context.view_layer.layer_collection.children[geometry_collection.name]
    geometry_layer.exclude=True
    try:
        actions,tracks=motion.animate(rig)
    finally:
        geometry_layer.exclude=False
    bpy.context.view_layer.update()
    print('Rendering inspection views',flush=True)
    camera=art.studio();camera.data.ortho_scale=1.48
    scene=bpy.context.scene;scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene.render.fps=60
    # Smaller studio lighting is adjusted for the gameplay asset's native scale.
    for light in scene.objects:
        if light.type=='LIGHT':light.location*=.4;light.data.energy*=.16;light.data.size*=.4;art.look_at(light,(0,0,.45))
    views=[('idle','Idle',88,(1.4,-2.2,1.0)),('front','Idle',60,(0,-2.2,.85)),('rear','Idle',60,(0,2.2,.85)),('side','Idle',60,(2.2,0,.85)),('walk','Walk',13,(1.4,-2.2,1.0)),('sit','Sit',78,(1.4,-2.2,1.0)),('groom','Groom',94,(1.4,-2.2,1.0)),('jump','Jump',23,(1.4,-2.2,1.0)),('claw','Claw',20,(1.4,-2.2,1.0)),('bite','Bite',20,(1.4,-2.2,1.0))]
    views.append(('face-detail','Idle',60,(.20,-2.2,.75)))
    if '--quick' in sys.argv:
        views=[view for view in views if view[0] in ('idle','front','face-detail')]
        scene.render.resolution_x=scene.render.resolution_y=700
    if '--no-previews' in sys.argv:views=[]
    for name,action,frame,view in views:
        rig.animation_data.action=actions[action];scene.frame_set(frame);camera.location=view;art.look_at(camera,(0,-.03,.47));camera.data.ortho_scale=1.48
        if name=='face-detail':
            art.look_at(camera,(0,-.39,.68));camera.data.ortho_scale=.58
        scene.render.filepath=os.path.join(PREVIEW,name+'.png');bpy.ops.render.render(write_still=True)
    rig.animation_data.action=None
    for track in tracks:track.mute=False
    scene.frame_set(1);bpy.ops.object.select_all(action='DESELECT')
    for obj in PARTS+[rig]:obj.select_set(True)
    bpy.context.view_layer.objects.active=rig
    path=os.path.join(MODEL,'tactical-tabby-game-cat.glb')
    bpy.ops.export_scene.gltf(filepath=path,export_format='GLB',use_selection=True,export_animations=True,export_nla_strips=True,export_frame_range=True,export_force_sampling=True,export_frame_step=1,export_skins=True,export_def_bones=True,export_yup=True,export_apply=False)
    with open(path,'rb') as file:binary=file.read()
    json_length=struct.unpack_from('<I',binary,12)[0]
    document=json.loads(binary[20:20+json_length])
    surface=next(m for m in document['materials'] if m['name']=='TacticalTabby.Fur.GroomedSurface')
    strands=next(m for m in document['materials'] if m['name']=='TacticalTabby.Fur.GroomedStrands')
    assert surface['pbrMetallicRoughness'].get('baseColorTexture') and surface.get('normalTexture')
    assert strands['pbrMetallicRoughness'].get('baseColorTexture') and strands.get('alphaMode')=='MASK'
    assert strands.get('doubleSided') and abs(strands.get('alphaCutoff',0)-.4)<1e-6
    for track in tracks:track.mute=True
    rig.animation_data.action=actions['Idle'];scene.frame_set(1);scene.frame_end=240
    camera.location=(1.4,-2.2,1.0);art.look_at(camera,(0,-.03,.47));camera.data.ortho_scale=1.48
    for area in bpy.context.screen.areas:
        if area.type=='VIEW_3D':
            area.spaces.active.region_3d.view_distance=1.7
            area.spaces.active.region_3d.view_location=Vector((0,-.03,.45))
            area.spaces.active.region_3d.view_rotation=camera.rotation_euler.to_quaternion()
            area.spaces.active.shading.type='MATERIAL'
    text=bpy.data.texts.new('START HERE - Playable Tactical Tabby');text.use_fake_user=True
    text.write('Original custom gameplay character. Seven clips: Idle, Walk, Sit, Groom, Jump, Claw, Bite.\n'
               'All NLA tracks are muted; Idle is the active Action. Choose one Action at a time to preview.\n'
               'Root motion is in place; gameplay supplies travel and jump height.\n'
               'Chonk shapes on torso/gear are driven by the game, not baked into the base model.\n'
               'Coat uses packed undercoat/normal maps and skinned alpha-masked strands. Editable PNGs: assets/models/textures/tactical-tabby.\n'
               'Save manual edits to a new copy before rebuilding with tools/build_tactical_game_cat.py.\n')
    reference=os.path.join(MODEL,'artist-work','tactical-tabby-soft','reference.jpg')
    if os.path.exists(reference):
        image=bpy.data.images.load(reference);image.name='Original character design reference';image.use_fake_user=True;image.pack()
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(MODEL,'tactical-tabby-game-cat.blend'))
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    for action in list(bpy.data.actions):bpy.data.actions.remove(action)
    bpy.ops.import_scene.gltf(filepath=path)
    meshes=[o for o in scene.objects if o.type=='MESH'];rigs=[o for o in scene.objects if o.type=='ARMATURE']
    clips=sorted(a.name for a in bpy.data.actions)
    report={'blender':bpy.app.version_string,'meshes':len(meshes),'triangles':sum(sum(len(f.vertices)-2 for f in o.data.polygons) for o in meshes),'bones':len(rigs[0].data.bones),'skinnedMeshes':sum(any(m.type=='ARMATURE' for m in o.modifiers) for o in meshes),'clips':clips,'coat':coat_report,'source':'Original character geometry based on user references; no canonical cat mesh reused'}
    report['glbSha256']=hashlib.sha256(binary).hexdigest()
    report['glbBytes']=len(binary)
    assert len(rigs)==1 and report['skinnedMeshes']==len(meshes)
    assert all(any(name in clip for clip in clips) for name in ('Idle','Walk','Groom','Sit','Jump','Claw','Bite'))
    with open(os.path.join(PREVIEW,'verification.json'),'w') as f:json.dump(report,f,indent=2)
    print('TACTICAL_GAME_CAT_VERIFIED',json.dumps(report),flush=True)


if __name__=='__main__':main()
