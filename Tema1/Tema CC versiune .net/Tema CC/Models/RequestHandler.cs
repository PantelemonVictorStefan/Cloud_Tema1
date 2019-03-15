using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net;
using System.Threading.Tasks;

namespace Tema_CC.Models
{
    public class RequestHandler
    {

        public byte[] content;
        public RequestHandler(string url)
        {
            var client = new WebClient();

            var x = new Stopwatch();
            x.Start();
            content = client.DownloadData(url);
            x.Stop();

            Logger.log(new LogInformation(url, content, x.ElapsedMilliseconds));
            client.Dispose();

        }
    }
}
