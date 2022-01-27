
// Breadth First Search function
// v is the source vertex
// all_pairs is the input array, which contains length 2 arrays
// visited is a dictionary for keeping track of whether a node is visited
var bfs = function(v, all_pairs, visited) {

    var q = [];
    var current_group = [];
    var i, nextVertex, pair;
    var length_all_pairs = all_pairs.length;
    q.push(v);
    while (q.length > 0) {
    v = q.shift();
    if (!visited[v]) {
      visited[v] = true;
      current_group.push(v);
      // go through the input array to find vertices that are
      // directly adjacent to the current vertex, and put them
      // onto the queue
      for (i = 0; i < length_all_pairs; i += 1) {
        pair = all_pairs[i];
        if (pair[0] === v && !visited[pair[1]]) {
          q.push(pair[1]);
        } else if (pair[1] === v && !visited[pair[0]]) {
          q.push(pair[0]);
        }
      }
    }
    }
    // return everything in the current "group"
    return current_group;
};

var createClusters = function(pairs) {

    var groups = [];
    var i, k, length, u, v, src, current_pair;
    var visited = {};

    for (i = 0, length = pairs.length; i < length; i += 1) {
      current_pair = pairs[i];
      u = current_pair[0];
      v = current_pair[1];
      src = null;
      if (!visited[u]) {
        src = u;
      } else if (!visited[v]) {
        src = v;
      }
      if (src) {
        // there is an unvisited vertex in this pair.
        // perform a breadth first search, and push the resulting
        // group onto the list of all groups
        groups.push(bfs(src, pairs, visited));
      }
    }
    return groups;
};


function changeValueOnSlider(value, network, limits) {

    var i, j, k, limit, countyName, countyItem;
    var edgeList = [];
    var clusters = [];
    var inCluster = [];

    limit = limits[value];
    document.getElementById('sliderValue').textContent = limit.toFixed(10);

    for (i = 0, length = network.length; i < length; i += 1) {
        if (network[i][2]['weight_new'] >= limit) {
            edgeList.push(network[i]);
        }
    }

    clusters = createClusters(edgeList);
    clusters.sort((a, b) => b.length - a.length);

    k = 0;

    for (i = 0, length_i = clusters.length; i < length_i; i += 1) {
        for (j = 0, length_j = clusters[i].length; j < length_j; j += 1) {
            countyName = clusters[i][j];
            countyItem = Object.keys(simplemaps_countrymap_mapdata.state_specific).find(key =>
            simplemaps_countrymap_mapdata.state_specific[key]["name"].toUpperCase() == countyName);
            inCluster.push(simplemaps_countrymap_mapdata.state_specific[countyItem]["name"]);
            simplemaps_countrymap_mapdata.state_specific[countyItem].color = colorList[k];
            simplemaps_countrymap_mapdata.state_specific[countyItem].hover_color = colorList[k];

        }
        k += 1;
    }

    for (countyItem in simplemaps_countrymap_mapdata.state_specific) {
        if (!inCluster.includes(simplemaps_countrymap_mapdata.state_specific[countyItem]["name"])){
            simplemaps_countrymap_mapdata.state_specific[countyItem].color = colorList[k];
            simplemaps_countrymap_mapdata.state_specific[countyItem].hover_color = colorList[k];

            k += 1;
        }

    }

    simplemaps_countrymap.refresh();
    hideText();
}


function hideText() {
    document.querySelector("#map > * a").setAttribute('style', 'visibility:hidden !important');
}