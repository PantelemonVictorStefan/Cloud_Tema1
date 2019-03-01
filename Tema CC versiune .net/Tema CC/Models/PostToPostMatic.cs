using System;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace Tema_CC.Models
{
    public class PostToPostMatic
    {
        public byte[] photo;
        public string res;

        public PostToPostMatic()
        {
            var rh= new RequestHandler("https://randomuser.me/api/");

            var wb = new WebClient();
            var url = "https://localhost:44388/post1";
            var data = new NameValueCollection();
            //data["username"] = "myUser";
            data["data"] = Encoding.UTF8.GetString(rh.content);

            var response = wb.UploadValues(url, "POST", data);
            string responseInString = Encoding.UTF8.GetString(response);
            res = responseInString;
            //res = response;
            /*
            var wb = new WebClient();
            wb.UploadData("https://localhost:44388/postPicture", rh.content);
            wb.Dispose();*/


        }
    }
}
