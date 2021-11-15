
scene = new THREE.Scene();
camera = new THREE.PerspectiveCamera(45,window.innerWidth / window.innerHeight,0.1 ,1000);
camera.position.z = 18.5;
camera.position.y = 2.7;
camera.position.x = 0.2;
renderer = new THREE.WebGLRenderer({alpha:true,antialias:true});
renderer.setClearColor(0x000000,0);
renderer.setSize(1920,1080);

renderer.domElement.setAttribute("id","Plant3DObj");
document.body.insertBefore(renderer.domElement, document.body.firstChild);

const aLight = new THREE.AmbientLight(0x404040,1.2);
scene.add(aLight);

const pLight = new THREE.PointLight(0xFFFFF,1.2);
pLight.position.set(-3,10,30);
scene.add(pLight);

const helper = new THREE.PointLightHelper(pLight);
scene.add(helper);

let loader = new THREE.GLTFLoader();
let obj = null;

loader.load('/static/3d/CircleOfThrees2.glb', function(gltf){
    obj = gltf;
    obj.scene.scale.set(1, 1, 1);
    scene.add(obj.scene);
})

function animate(){
    requestAnimationFrame(animate);
    if(obj)
        obj.scene.rotation.y +=0.0002;
    renderer.render(scene , camera)
}
animate();
