var xml = "packages2.5.xml"
var num_pkg = 0;

var conn = new XMLHttpRequest();
conn.open("GET", xml, false);
conn.onreadystatechange = function () {
  if (conn.readyState == 4 && conn.status == 200) {
    document.write('<table border="1">');
    //header
    document.write("<tr><th>");
    document.write("Package");
    document.write("</th><th>");
    document.write("Version");
    document.write("</th><th>");
    document.write("Description");
    document.write("</th><th>");
    document.write("Dependency");
    document.write("</th></tr>");

    var doc = conn.responseXML;
    var packages = doc.getElementsByTagName("package");
    for (var pk in packages) {
        var name = packages[pk].getAttribute("name");
        var version = packages[pk].getAttribute("version");
		var projectURL = packages[pk].getAttribute("projectURL");
		var description = packages[pk].getAttribute("description");
		// Write the data to the page.
		document.write("<tr><td>");
		document.write("<a href=\"" + projectURL + "\">" + name + "</a>");
		document.write("</td><td>");
		document.write(version);
		document.write("</td><td>");
		document.write(description);
		document.write("</td><td>");
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
		document.write(dependency);
		document.write("</td></tr>");
		num_pkg ++;				
    }
    document.write('</table>');
    var num = packages.length;
//     document.write('<p>num.toString().concat(" packages")</p>');
  } else if (xmlhttp.status==404) { 
    alert(xml.concat(" could not be found")); 
  }
};
conn.send(null);

document.write("<p>Extract " + num_pkg + " packages from " + xml + "</p>");

