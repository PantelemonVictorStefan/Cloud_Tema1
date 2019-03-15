using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using System.Xml.Serialization;

namespace PostMatic.Models
{
    public static class UserManager
    {
        public static List<string> users = new List<string>();

        private static void saveLogs()
        {
            XmlSerializer mySerializer = new XmlSerializer(typeof(List<string>));
            StreamWriter myWriter = new StreamWriter("users.xml");
            mySerializer.Serialize(myWriter, UserManager.users);
            myWriter.Close();
        }

        private static bool loadUsers()
        {
            if (!File.Exists("users.xml"))
            {
                UserManager.users = new List<string>();
                return false;
            }
            XmlSerializer mySerializer = new XmlSerializer(typeof(List<string>));
            StreamReader myReader = new StreamReader("users.xml");
            UserManager.users = (List<string>)mySerializer.Deserialize(myReader);
            myReader.Close();
            return true;
        }

        public static void AddUser(string info)
        {
            loadUsers();
            users.Add(info);
            saveLogs();
        }

        public static List<string> GetUsers()
        {
            loadUsers();
            return UserManager.users;
        }

    }
}
