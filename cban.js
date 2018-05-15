
// Walter Xie
// May 2018

// Package obj
function Package(name, version, projectURL, description, depends){
  this.name = name;
  this.version = version;
  this.projectURL = projectURL;
  this.description = description;
  this.depends = depends;
  this.fullName = function(){
    return this.name + ":" + this.version;
  } 
  this.dependency = function(){
    var depStr = "";
	for(var i = 0; i < depends.length; i++) {
	  if (i > 0) {
		  depStr = depStr + ", ";
	  }
	  depStr = depStr + depends[i].getAttribute("on") + " (" + depends[i].getAttribute("atleast");
	  if (depends[i].hasAttribute("atmost")) {       
		  depStr = depStr + "-" + depends[i].getAttribute("atmost") + ")";
	  } else {
		  depStr = depStr + "-?)";
	  }
	}
	return depStr;
  } 
} 

// parse packages XML from CBAN
function getPackagesFromXML(xml, unique) {
	var packagesDict = {};
    
    var conn = new XMLHttpRequest();
	conn.open("GET", xml, false);
	conn.onreadystatechange = function () {
	  if (conn.readyState == 4 && conn.status == 200) {
		var doc = conn.responseXML;
		var i, pkgs = doc.getElementsByTagName("package");
		for (i = 0; i < pkgs.length; i++) { 
// 			var name = pkgs[i].getAttribute("name");
// 			var version = pkgs[i].getAttribute("version");
// 			var projectURL = pkgs[i].getAttribute("projectURL");
// 			var description = pkgs[i].getAttribute("description");
// 			var depends = pkgs[i].getElementsByTagName("depends");
			// package Obj
			var pkg = new Package(pkgs[i].getAttribute("name"), pkgs[i].getAttribute("version"),
				pkgs[i].getAttribute("projectURL"),pkgs[i].getAttribute("description"),
				pkgs[i].getElementsByTagName("depends"));
						
			// Write the data to dict
			packagesDict[pkg.fullName()] = pkg;

		}
// 		console.log(packagesDict);
	  } else if (xmlhttp.status==404) { 
		alert(xml.concat(" could not be found")); 
	  }
	};
	conn.send(null);
	return packagesDict;
}


// print packages to html
function printTable(divname) {
	var xml = document.getElementById("xml").value;
	var unique = document.getElementById("unique").checked;
    // a dict, key is name:version, value is a Package obj
    var packagesDict = getPackagesFromXML(xml, unique);
        
    var html = "<table border=\"1\">";
	//header
	html += "<tr><th>";
	html += "Package";
	html += "</th><th>";
	html += "Version";
	html += "</th><th>";
	html += "Description";
	html += "</th><th>";
	html += "Dependency";
	html += "</th></tr>";
    
    var num_pkg = 0;
    // ECMAScript 2017
	for (const [key, pkgObj] of Object.entries(packagesDict)) {
		// Write the data to the page.
		html += "<tr><td>";
		html += "<a href=\"" + pkgObj.projectURL + "\">" + pkgObj.name + "</a>";
		html += "</td><td>";
		html += pkgObj.version;
		html += "</td><td>";
		html += pkgObj.description;
		html += "</td><td>";
		html += pkgObj.dependency();
		html += "</td></tr>";
		num_pkg ++;				
	}
	html += '</table>';

	html = "<p>Extract " + num_pkg + " packages from " + xml + "</p>" + html;
	
    document.getElementById(divname).innerHTML = html;
}