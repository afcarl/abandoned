#import('dart:html');
#import('dart:json');

#source('requests.dart');
#source('views.dart');
#source('models.dart');

final String ENTRIES_URL = 'http://localhost:8080/api/entries';
final int FETCH_COUNT = 3;

final String ENTRIES_PREFIX = '#entries';
final String ARCHIVE_PREFIX = '#archive';

PagesView pagesView;

void navigate(String hash) {
  if (hash == '' || hash == '#') {
    loadEntry(null, (entry) => pagesView.page = entry);
  } else {
    if (hash.startsWith(ENTRIES_PREFIX)) {
      List<String> tokens = hash.split('/');
      if (tokens.length > 1 && tokens[1] != '') {
        loadEntry(tokens[1], (entry) => pagesView.page = entry);
      } else {
        loadEntry(null, (entry) => pagesView.page = entry);
      }
    } else if (hash.startsWith(ARCHIVE_PREFIX)) {
      // TODO
    }
  }
}

void main() {
  Element title = document.query('#main-title');
  Element container = document.query('#main-container');
  pagesView = new PagesView();
  container.nodes.add(pagesView.container);

  navigate(window.location.hash);
  window.on.hashChange.add((e) {
    navigate(window.location.hash);
  });
}
