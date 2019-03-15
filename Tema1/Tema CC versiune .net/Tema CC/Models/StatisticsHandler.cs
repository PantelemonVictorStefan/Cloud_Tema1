using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;


namespace Tema_CC.Models
{
    public class StatisticsHandler
{
        public StatisticsHandler()
        {

        }

        public string GetStatisticsAsJson()
        {
            var logs = Logger.getLogs();
            var urlLatency = new Dictionary<string, long>();
            var urlCount = new Dictionary<string, int>();

            foreach (LogInformation i in logs)
            {
                if (!urlLatency.Keys.Contains(i.request))
                {
                    urlLatency[i.request] = i.latency;
                    urlCount[i.request] = 1;
                }
                else
                {
                    urlLatency[i.request] += i.latency;
                    urlCount[i.request]++;
                }
            }


            var statisticsData = new List<LogInformation>();
            foreach (KeyValuePair<string, long> entry in urlLatency.ToList())
            {
                urlLatency[entry.Key] = entry.Value / urlCount[entry.Key];
                statisticsData.Add(new LogInformation(entry.Key, null, urlLatency[entry.Key]));
            }

            


            return Newtonsoft.Json.JsonConvert.SerializeObject(statisticsData);
        }
}
}
