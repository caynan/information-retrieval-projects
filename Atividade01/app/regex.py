# text to lowercase and remove white trailing spaces
text = text.lower().strip()
text = re.sub("&.{2,4};", " ", text)
text = re.sub("\\{\\{!\\}\\}", " ", text)
# Remove text in the format {{ ... }}
text = re.sub("{{.*?}}", "", text)
# Remove markup tags in the format <foo> OR </foo>
text = re.sub("<.*?>", "", text)
# remove all non alphanumeric characters
text = re.sub("[^a-z0-9çáéíóúàãõâêô-]", " ", text)

