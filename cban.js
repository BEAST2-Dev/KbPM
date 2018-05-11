var xml = "packages2.5.xml"

var conn = new XMLHttpRequest();
conn.open("GET", xml, false);
conn.onreadystatechange = function () {
  if (conn.readyState == 4 && conn.status == 200) {
    var doc = conn.responseXML;
    var packages = doc.getElementsByTagName("package")
    document.write('<table border="1">');
    for (var pk in packages) {
        var name = packages[pk].getAttribute("name");
        var version = packages[pk].getAttribute("version");
		var projectURL = packages[pk].getAttribute("projectURL");
		// Write the data to the page.
		document.write("<tr><td>");
		document.write(name);
		document.write("</td><td>");
		document.write(version);
		document.write("</td><td>");
		document.write(projectURL);
		document.write("</td></tr>");
    }
    document.write('</table>');
    var num = packages.length;
//     document.write('<p>num.toString().concat(" packages")</p>');
  } else if (xmlhttp.status==404) { 
    alert(xml.concat(" could not be found")); 
  }
};
conn.send(null);
