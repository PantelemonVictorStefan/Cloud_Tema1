using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace PostMatic.Models
{
    public class MyFile
    {
        public string userId { get; set; }
        public Microsoft.AspNetCore.Http.IFormFile File { get; set; }
        // Other properties
    }
}
