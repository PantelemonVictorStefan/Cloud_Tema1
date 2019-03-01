using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Tema_CC.Models;

namespace Tema_CC.Controllers
{
    [Route("getStatistics")]
    public class StatisticsController : Controller
    {
        [HttpGet]
        public string GetStatistics()
        {
            return new StatisticsHandler().GetStatisticsAsJson();

        }
    }
}
