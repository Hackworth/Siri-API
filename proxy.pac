function FindProxyForURL(url, host)
{
  var keyword = url.toLowerCase().indexOf("<keyword>");
  if (dnsDomainIs(host, "<google_domain>") && (keyword >= 0) && url.toLowerCase().indexOf("search?q=") >= 0)	{
    return "PROXY <squid_host>:<squid_port>";
  }
  if (dnsDomainIs(host, "<yahoo_domain>") && url.toLowerCase().indexOf("search?p=") >= 0)	{
    return "PROXY <squid_host>:<squid_port>";
  }
  return "DIRECT";
}
