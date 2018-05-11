var xml = "packages2.5.xml"
// Create a connection to the file.
var Connect = new XMLHttpRequest();
// Define which file to open and
// send the request.
Connect.open("GET", xml, false);
Connect.setRequestHeader("Content-Type", "xml");
Connect.send(null);

if (Connect.readyState == 4 && Connect.status == 200) {
	// Place the response in an XML document.
	var TheDocument = Connect.responseXML;
	// Place the root node in an element.
	var Packages = TheDocument.childNodes[0];
	// Retrieve each customer in turn.
	for (var i = 0; i < Packages.children.length; i++) {
		var Package = Packages.children[i];
		// Access each of the data values.
		var name = Package.getElementsByTagName("name");
		var version = Package.getElementsByTagName("version");
		var projectURL = Package.getElementsByTagName("projectURL");
		// Write the data to the page.
		document.write("<tr><td>");
		document.write(name[0].textContent.toString());
		document.write("</td><td>");
		document.write(version[0].textContent.toString());
		document.write("</td><td>");
		document.write(projectURL[0].textContent.toString());
		document.write("</td></tr>");
	}
} else if (xmlhttp.status==404) { 
    alert(xml.concat(" could not be found")); 
}