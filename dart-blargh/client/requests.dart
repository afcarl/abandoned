
String escape(String data) {
  return data.replaceAll(':', '%3A')
             .replaceAll('/', '%2F')
             .replaceAll('?', '%3F')
             .replaceAll('=', '%3D')
             .replaceAll('&', '%26')
             .replaceAll(' ', '%20')
             .replaceAll('\$', '%24')
             .replaceAll('+', '%2B')
             .replaceAll(',', '%2C')
             .replaceAll(';', '%3B')
             .replaceAll('@', '%40');
}

String urlEncode(Map data) {
  List<String> tokens = [];
  data.forEach((key, value) => tokens.add('${key}=${value}'));
  return Strings.join(tokens, '&');
}
