using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;
using Tema_CC.Models;

namespace Tema_CC.Controllers
{
    [Route("generateImage")]
    public class RandomPeople : Controller
{
    [HttpGet]
    public ActionResult GetResult()
    {
            var x = new RequestHandler("https://thispersondoesnotexist.com/image");
            return File(x.content, "image/jpeg");
    }
}
}