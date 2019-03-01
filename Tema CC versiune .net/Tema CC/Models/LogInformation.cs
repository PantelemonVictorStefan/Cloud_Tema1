using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Tema_CC.Models
{
    public class LogInformation
{
        public string request;
        public byte[] response;
        public long latency;

        public LogInformation()
        {

        }

        public LogInformation(string req,byte[] res,long lat)
        {
            request = req;
            response = res;
            latency = lat;
        }
}
}
