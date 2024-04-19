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
const formatTimeOptions = {
  hour: "2-digit",
  minute: "2-digit",
};
const timeFormat = new Intl.DateTimeFormat("ru-RU", formatTimeOptions).format;

export { wsUri, timeFormat };
