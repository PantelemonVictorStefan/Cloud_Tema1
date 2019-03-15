using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Threading.Tasks;
using Tema_CC.Models;

namespace Tema_CC.Controllers
{
    [Route("postToPostMatic")]
    public class PostPictures : Controller
    {
        [HttpPost]
        public void GetResult()
        {
            var x = new PostToPostMatic();
            //return x.res;
            //var res = new RequestHandler("https://localhost:44388/htmlpage.html");
        }
    }
}
