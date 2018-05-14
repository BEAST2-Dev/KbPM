
// print packages given a xml from CBAN
// Walter Xie
// May 2018
function printTable(divname) {
	var xml = document.getElementById("xml").value;
    var num_pkg = 0;
    var html;

	var conn = new XMLHttpRequest();
	conn.open("GET", xml, false);
	conn.onreadystatechange = function () {
	  if (conn.readyState == 4 && conn.status == 200) {
		html = "<table border=\"1\">";
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

		var doc = conn.responseXML;
		var packages = doc.getElementsByTagName("package");
		for (var pk in packages) {
			var name = packages[pk].getAttribute("name");
			var version = packages[pk].getAttribute("version");
			var projectURL = packages[pk].getAttribute("projectURL");
			var description = packages[pk].getAttribute("description");
			// Write the data to the page.
			html += "<tr><td>";
			html += "<a href=\"" + projectURL + "\">" + name + "</a>";
			html += "</td><td>";
			html += version;
			html += "</td><td>";
			html += description;
			html += "</td><td>";
			// dependency
			var dependency="", depends = packages[pk].getElementsByTagName("depends");
			for(var i = 0; i < depends.length; i++) {
			  if (i > 0) {
				  dependency = dependency + ", ";
			  }
			  dependency = dependency + depends[i].getAttribute("on") + " (" + depends[i].getAttribute("atleast");
			  if (depends[i].hasAttribute("atmost")) {       
				  dependency = dependency + "-" + depends[i].getAttribute("atmost") + ")";
			  } else {
				  dependency = dependency + "-?)";
			  }
			}
			html += dependency;
			html += "</td></tr>";
			num_pkg ++;				
		}
		html += '</table>';
		var num = packages.length;
	//     html += '<p>num.toString().concat(" packages")</p>');
	  } else if (xmlhttp.status==404) { 
		alert(xml.concat(" could not be found")); 
	  }
	};
	conn.send(null);

	html = "<p>Extract " + num_pkg + " packages from " + xml + "</p>" + html;
	
    document.getElementById(divname).innerHTML = html;
}