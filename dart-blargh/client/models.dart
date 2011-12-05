
class BlogEntry implements Page {
  final String keyname;
  final String title;
  final String content;
  final List<String> labels;
  final List<String> links;
  final Date date;
  final String previousKeyname;
  final String nextKeyname;
  
  BlogEntry(this.keyname,
            this.previousKeyname,
            this.nextKeyname,
            this.title,
            this.content,
            this.labels,
            this.links,
            this.date);
  
  factory BlogEntry.map(Map entry) {
    String keyname = entry['keyname'];
    String prev = entry['prev'];
    String next = entry['next'];
    String title = entry['title'];
    String content = entry['content'];
    Date date = new Date.fromString(entry['created']);
    List<String> labels = entry['labels'];
    List<String> links = entry['links'];
    return new BlogEntry(keyname, prev, next, title, content, labels, links, date);
  }
  
  // Page methods
  String get previousToken() => previousKeyname == null ? null : '#entries/${previousKeyname}';
  String get nextToken() => nextKeyname == null ? null : '#entries/${nextKeyname}';
  View get view() => new BlogEntryView(this);
}

void loadEntry(String keyname, void callback(BlogEntry entry)) {
  XMLHttpRequest req = new XMLHttpRequest();
  req.on.load.add((event) {
    List<Map> data = JSON.parse(req.responseText);
    List<BlogEntry> entries = new List();
    data.forEach((map) => entries.add(new BlogEntry.map(map)));
    entries.sort((e1, e2) => e1.date.compareTo(e2.date));
    if (entries.length > 0) {
      callback(entries.last());
    }
  });
  
  if (keyname == null) {
    req.open('GET', '${ENTRIES_URL}', true);
  } else {
    req.open('GET', '${ENTRIES_URL}/${keyname}', true);
  }
  
  req.send();
}
