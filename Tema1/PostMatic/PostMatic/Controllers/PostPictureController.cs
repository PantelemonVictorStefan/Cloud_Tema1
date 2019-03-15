using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using PostMatic.Models;

namespace PostMatic.Controllers
{
    //[Route("postPicture")]
    public class PostPictureController : Controller
    {
        [HttpPost("post1")]
        public HttpStatusCode PostPicture(string data)
        {

            UserManager.AddUser(data);
            //return View();
            return HttpStatusCode.OK;
        }

        [HttpPost("post2")]
        public async void UploadImage(MyFile upload)
        {
            var file = upload.File; // This is the IFormFile file
            var param = upload.userId; // param
            using (var stream = new System.IO.FileStream("images", FileMode.Create))
            {
                await file.CopyToAsync(stream);
            }
            //return upload.File.Length;
        }
    }
}