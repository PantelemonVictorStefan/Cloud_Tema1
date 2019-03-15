using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using System.Xml.Serialization;

namespace Tema_CC.Models
{
    public static class Logger
{
        public static List<LogInformation> logs=new List<LogInformation>();

        private static void saveLogs()
        {
            XmlSerializer mySerializer = new XmlSerializer(typeof(List<LogInformation>));
            StreamWriter myWriter = new StreamWriter("logs.xml");
            mySerializer.Serialize(myWriter, Logger.logs);
            myWriter.Close();
        }

        private static bool loadLogs()
        {
            if (!File.Exists("logs.xml"))
            {
                Logger.logs = new List<LogInformation>();
                return false;
            }
            XmlSerializer mySerializer = new XmlSerializer(typeof(List<LogInformation>));
            StreamReader myReader = new StreamReader("logs.xml");
            Logger.logs = (List<LogInformation>)mySerializer.Deserialize(myReader);
            myReader.Close();
            return true;
        }

        public static void log(LogInformation info)
        {
            loadLogs();
            logs.Add(info);
            saveLogs();
        }

        public static List<LogInformation> getLogs()
        {
            loadLogs();
            return Logger.logs;
        }

}
}
