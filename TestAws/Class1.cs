using NUnit.Framework;
using System;
using System.Net.NetworkInformation;

namespace TestAws
{
    public class Class1
    {
        [Test]
        [Category("sanity")]
        public void Test1()
        {
            var url = TestContext.Parameters.Get("url", "");
            Console.WriteLine($"PVWA url is {url}");
            Assert.True(!String.IsNullOrEmpty(url));
            var pinger = new Ping();
            PingReply reply = pinger.Send(url);
            var pingable = reply.Status == IPStatus.Success;
            Console.WriteLine($"PVWA url is {url}");
            Assert.True(pingable, "check if pingable");
        }
    }
}
