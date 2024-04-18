export function stringLimit(str, limit) {
  return str.length > limit ? str.substring(0, limit) + "..." : str;
}

var loc = window.location,
  wsUri;
if (loc.protocol === "https:") {
  wsUri = "wss:";
} else {
  wsUri = "ws:";
}
//wsUri += "//" + loc.host;
wsUri += "//" + "localhost:8000";

export { wsUri };
