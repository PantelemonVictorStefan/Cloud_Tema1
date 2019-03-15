using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using PostMatic.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PostMatic.Controllers
{
    public class GetUsersController:Controller
    {
        [HttpGet("getUsers")]
        public ActionResult GetUsers()
        {

            
            return File(Encoding.UTF8.GetBytes(JsonConvert.SerializeObject(UserManager.GetUsers())), "application/json");
        }
    }
}
