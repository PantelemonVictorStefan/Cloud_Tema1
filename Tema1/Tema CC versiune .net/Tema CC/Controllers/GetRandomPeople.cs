using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Tema_CC.Models;

namespace Tema_CC.Controllers
{
    [Route("getRandomPeople")]
    public class GetRandomPeople : Controller
    {
        [HttpGet]
        public ActionResult GetResult()
        {
            var x = new RequestHandler("https://randomuser.me/api/");
            return File(x.content,"application/json");
        }
    }
}