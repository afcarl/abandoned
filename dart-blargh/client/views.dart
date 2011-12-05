
interface View {
  Element get container();
}

class BlogEntryView implements View {
  final BlogEntry entry;
  final Element container;
  
  Element _title(String title) {
    Element header = new Element.tag('h2');
    header.classes.add('blogEntry-title');
    header.innerHTML = title;
    return header;
  }
  
  Element _date(Date date) {
    Element date = new Element.tag('div');
    date.classes.add('blogEntry-date');
    date.innerHTML = date.toString();
    return date;
  }
  
  Element _content(String content) {
    Element elem = new Element.tag('div');
    elem.classes.add('blogEntry-content');
    elem.innerHTML = content;
    return elem;
  }
  
  Element _labels(List<String> labels) {
    Element tags = new Element.tag('div');
    tags.classes.add('blogEntry-labels');
    
    Element tagsHeader = new Element.tag('div');
    tagsHeader.classes.add('blogEntry-labels-header');
    tagsHeader.innerHTML = 'Labels:';
    tags.nodes.add(tagsHeader);
    
    Element tagsList = new Element.tag('div');
    tagsList.classes.add('blogEntry-labels-list');
    tagsList.innerHTML = Strings.join(entry.labels, ', ');
    tags.nodes.add(tagsList);
    
    return tags;
  }
  
  Element _links(List<String> links) {
    Element elem = new Element.tag('div');
    elem.classes.add('blogEntry-links');
    
    Element linksHeader = new Element.tag('div');
    linksHeader.classes.add('blogEntry-links-header');
    linksHeader.innerHTML = 'References:';
    elem.nodes.add(linksHeader);
    
    Element linksList = new Element.tag('ul');
    linksList.classes.add('blogEntry-links-list');
    elem.nodes.add(linksList);
    
    links.forEach((link) {
      Element linkElem = new Element.tag('li');
      linksList.nodes.add(linkElem);
      Element linkHref = new Element.tag('a');
      linkHref.attributes['href'] = link;
      linkHref.innerHTML = link;
      linkElem.nodes.add(linkHref);
    });
    
    return elem;
  }
  
  BlogEntryView(this.entry) : container = new Element.tag('div') {
    container.classes.add('blogEntry');
    container.nodes.add(_title(entry.title));
    container.nodes.add(_date(entry.date));
    container.nodes.add(_content(entry.content));
    container.nodes.add(_labels(entry.labels));
    container.nodes.add(_links(entry.links));
  }
}

interface Page {
  View get view();
  String get nextToken();
  String get previousToken();
}

class PagesView implements View {
  final Element container;
  final Element _pageContainer;
  final Element _nextItem;
  final Element _nextLink;
  final Element _previousItem;
  final Element _previousLink;
  
  Page _currentPage;
  
  PagesView()
    : container = new Element.tag('div'), 
      _pageContainer = new Element.tag('div'), 
      _nextItem = new Element.tag('li'),
      _nextLink = new Element.tag('a'),
      _previousItem = new Element.tag('li'),
      _previousLink = new Element.tag('a') {

    _pageContainer.classes.add('pagesView');
    _pageContainer.classes.add('well');
    container.nodes.add(_pageContainer);
    
    Element _paginator = new Element.tag('div');
    _paginator.classes.add('pagination');
    container.nodes.add(_paginator);
    
    Element list = new Element.tag('ul');
    _paginator.nodes.add(list);
    
    _previousItem.classes.add('prev');
    _previousItem.classes.add('disabled');
    list.nodes.add(_previousItem);
    
    _previousLink.innerHTML = 'Previous';
    _previousItem.nodes.add(_previousLink);
    
    _nextItem.classes.add('next');
    _nextItem.classes.add('disabled');
    list.nodes.add(_nextItem);
    
    _nextLink.innerHTML = 'Next';
    _nextItem.nodes.add(_nextLink);
  }
  
  Page get page() => _currentPage;
  
  void set page(Page page) {
    _pageContainer.nodes.clear();
    if (page != null) {
      if (page.previousToken == null) {
        _previousItem.classes.add('disabled');
        _previousLink.attributes.remove('href');
      } else {
        _previousItem.classes.remove('disabled');
        _previousLink.attributes['href'] = page.previousToken;
      }
      
      if (page.nextToken == null) {
        _nextItem.classes.add('disabled');
        _nextLink.attributes.remove('href');
      } else {
        _nextItem.classes.remove('disabled');
        _nextLink.attributes['href'] = page.nextToken;
      }
      
      _pageContainer.nodes.add(page.view.container);
      _currentPage = page;
    } else {
      _previousItem.classes.add('disabled');
      _nextItem.classes.add('disabled');
    }
  }
}
