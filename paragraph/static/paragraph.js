function fillSlots(data) {
    for (let key in data) {
        let value = data[key];
        $(key).html(value);
    }
}

function show_detail(path) {
    $.get(path, function (data) {
        $('#action').html(data);
    })
}

var node_3d_callback = function (node, event) {
    var path = '/edit_node/' + node.id;
    show_detail(path);
}

var add_node = function () {
    $.get('/add_node', function (data) {
        //location.reload();
        var node_id = data;
        node_callback('n' + node_id);
    })
}
var start_3d = function () {
    var div = document.getElementById('samplediv');
    div.style.height = '1em';
    var em = div.offsetHeight;

    var myGraph = ForceGraph3D({controlType: 'orbit'});
    //var myGraph = ForceGraph3D();
    var canvas = document.getElementById('3d-graph');
    var data = JSON.parse($('#3d-graph-data').text());

    console.log(data);
    mg = myGraph(canvas);
    console.log(em);
    mg.height(40 * em);
    mg.width(50 * em);
    mg.cooldownTicks(100);
    mg.backgroundColor('#FFFFFF')

    mg.graphData(data);
    mg.nodeAutoColorBy('name');
    mg.nodeThreeObject(node => {
        // use a sphere as a drag handle
        const obj = new THREE.Mesh(
            new THREE.SphereGeometry(10),
            new THREE.MeshBasicMaterial({depthWrite: false, transparent: true, opacity: 0})
        );

        // add text sprite as child
        const sprite = new SpriteText(node.name);
        sprite.color = node.color;
        sprite.textHeight = 6;
        obj.add(sprite);

        return obj;
    });
    mg.onNodeClick(node_3d_callback);
    mg.onNodeHover(function () {
    });
    mg.linkThreeObjectExtend(true);
    mg.linkThreeObject(link => {
        // extend link with text sprite
        const sprite = new SpriteText(`${link.reltype}`);
        sprite.color = 'darkgrey';
        sprite.textHeight = 3.5;
        return sprite;
    })
        .linkPositionUpdate((sprite, {start, end}) => {
            const middlePos = Object.assign(...['x', 'y', 'z'].map(c => ({
                [c]: start[c] + (end[c] - start[c]) / 2 // calc middle point
            })));

            // Position sprite
            Object.assign(sprite.position, middlePos);
        });
    //mg.linkDirectionalParticles(5);
    mg.d3Force('charge').strength(-120);
    mg
        //.linkWidth(1)
        .linkCurvature(0)
        .linkDirectionalArrowLength(3.5)
        .linkDirectionalArrowRelPos(1)
        .linkDirectionalArrowColor(function (link) {
            return "lightgrey"
        })
        .linkColor(function (link) {
            return "darkgrey"
        })
        //.linkAutoColorBy('reltype')
        .linkOpacity(0.3)
    ;
    mg.onNodeDragEnd(node => {
          node.fx = node.x;
          node.fy = node.y;
          node.fz = node.z;
        })
    mg.onEngineStop(() => mg.zoomToFit(400));
}
