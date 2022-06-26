using Android.App;
using Android.Content;
using Android.Content.PM;
using Android.OS;
using Android.Runtime;
using Android.Views;
using Android.Widget;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace ProjectCurs
{
    [Activity(Label = "Статистика", ConfigurationChanges = ConfigChanges.ScreenSize | ConfigChanges.Orientation, ScreenOrientation = ScreenOrientation.Locked)]
    public class statistics : Activity
    {
        static public IList<string> achievelist = new List<string>();
        protected override void OnCreate(Bundle savedInstanceState)
        {
            base.OnCreate(savedInstanceState);
            SetContentView(Resource.Layout.statistics);
            Button continuegoal = FindViewById<Button>(Resource.Id.buttonContinueGoal);
            IList<string> stringsinput = new List<string>();
            if (Intent.GetStringArrayListExtra("stringsinput") != null)
                stringsinput = Intent.Extras.GetStringArrayList("stringsinput");
            if (Intent.GetStringArrayListExtra("achievelist") != null && Intent.GetStringArrayListExtra("achievelist").Count != 0)
                achievelist = Intent.Extras.GetStringArrayList("achievelist");
            TextView difficultStat = FindViewById<TextView>(Resource.Id.difficultStat);
            TextView minDifficultStat = FindViewById<TextView>(Resource.Id.minDifficultStat);
            TextView maxDifficultStat = FindViewById<TextView>(Resource.Id.maxDifficultStat);
            TextView howMuchGoals = FindViewById<TextView>(Resource.Id.HowMuchGoals);
            TextView howMuchGoalsCompleted = FindViewById<TextView>(Resource.Id.HowMuchGoalsCompleted);
            TextView howMuchGoalsNotCompleted = FindViewById<TextView>(Resource.Id.HowMuchGoalsNotCompleted);
            TextView averageTimeToComplete = FindViewById<TextView>(Resource.Id.averageTimeToComplete);
            TextView howMuchTimeRemain1 = FindViewById<TextView>(Resource.Id.HowMuchTimeRemain1);
            TextView howMuchTimeRemain2 = FindViewById<TextView>(Resource.Id.HowMuchTimeRemain2);
            TextView howMuchTimeRemain11 = FindViewById<TextView>(Resource.Id.howMuchTimeRemain11);
            TextView howMuchTimeRemain22 = FindViewById<TextView>(Resource.Id.howMuchTimeRemain22);
            difficultStat.Text = AverageDifficult(stringsinput);
            minDifficultStat.Text = MinimumDifficult(stringsinput);
            maxDifficultStat.Text = MaximumDifficult(stringsinput);
            howMuchGoals.Text = GoalsCount(stringsinput);
            howMuchGoalsCompleted.Text = DoneCount(stringsinput);
            howMuchGoalsNotCompleted.Text = UnDoneCount(stringsinput);
            if (AverageFinish(stringsinput) == "0")
                averageTimeToComplete.Text = "–";
            else
                averageTimeToComplete.Text = AverageFinish(stringsinput);
            if (LatestDate1(stringsinput) == "0")
                howMuchTimeRemain1.Text = "–";
            else
                howMuchTimeRemain1.Text = LatestDate1(stringsinput);
            if (EarliestDate1(stringsinput) == "1000000000")
                howMuchTimeRemain2.Text = "–";
            else
                howMuchTimeRemain2.Text = EarliestDate1(stringsinput);
            if (LatestDate11(stringsinput) == "")
                howMuchTimeRemain11.Text = "–";
            else
                howMuchTimeRemain11.Text = LatestDate11(stringsinput);
            if (EarliestDate11(stringsinput) == "")
                howMuchTimeRemain22.Text = "–";
            else
                howMuchTimeRemain22.Text = EarliestDate11(stringsinput);
            continuegoal.Click += (o, e) =>
            {
                var intent = new Intent(this, typeof(MainActivity));
                intent.PutStringArrayListExtra("stringsinput", stringsinput);
                intent.PutStringArrayListExtra("achievelist", achievelist);
                StartActivity(intent);
            };
            // Create your application here
        }
        static string AverageDifficult(IList<string> goalsList) // Среднее значение сложности
        {
            double avarageDiff = 0;
            for (int i = 0; i < goalsList.Count; i++)
            {
                if (i % 4 == 3)
                    avarageDiff += Convert.ToInt32(goalsList[i]);
            }

            return Convert.ToString(Math.Round(avarageDiff / (goalsList.Count / 4), 1));
        }
        static string MinimumDifficult(IList<string> goalsList) // Минимальная сложность
        {
            int minDiff = 20;
            for (int i = 0; i < goalsList.Count; i++)
            {
                if (i % 4 == 3)
                {
                    if (Convert.ToInt32(goalsList[i]) < minDiff)
                        minDiff = Convert.ToInt32(goalsList[i]);
                }
            }

            return Convert.ToString(minDiff);
        }

        static string MaximumDifficult(IList<string> goalsList) // Максимальная сложность
        {
            int maxDiff = -1;
            for (int i = 0; i < goalsList.Count; i++)
            {
                if (i % 4 == 3)
                {
                    if (Convert.ToInt32(goalsList[i]) > maxDiff)
                        maxDiff = Convert.ToInt32(goalsList[i]);
                }
            }

            return Convert.ToString(maxDiff);
        }

        static string GoalsCount(IList<string> goalsList) // Общее количество целей
        {
            return Convert.ToString(goalsList.Count / 4);
        }

        static string DoneCount(IList<string> goalsList) // Количество выполненных
        {
            int doneCount = 0;
            for (int i = 0; i < goalsList.Count; i++)
            {
                if (i % 4 == 2)
                {
                    if (Convert.ToInt32(goalsList[i]) == 0)
                        doneCount++;
                }
            }

            return Convert.ToString(doneCount);
        }

        static string UnDoneCount(IList<string> goalsList) // Количество невыполненных
        {
            int unDoneCount = 0;
            for (int i = 0; i < goalsList.Count; i++)
            {
                if (i % 4 == 2)
                {
                    if (Convert.ToInt32(goalsList[i]) > 0)
                        unDoneCount++;
                }
            }

            return Convert.ToString(unDoneCount);
        }

        static string AverageFinish(IList<string> goalsList) // Среднее время до выполнения всех целей
        {
            double avarageFin = 0;
            for (int i = 0; i < goalsList.Count; i++)
            {
                if (i % 4 == 2)
                    avarageFin += Convert.ToInt32(goalsList[i]);
            }

            return Convert.ToString(Math.Round(avarageFin / (goalsList.Count / 4), 0));
        }

        static string LatestDate1(IList<string> goalsList) // До выполнения самой поздней цели
        {
            int latestDate = 0;
            string goalTitle = "";
            for (int i = 0; i < goalsList.Count; i++)
            {
                if (i % 4 == 2)
                {
                    if (Convert.ToInt32(goalsList[i]) > latestDate)
                    {
                        latestDate = Convert.ToInt32(goalsList[i]);
                        goalTitle = Convert.ToString(goalsList[i - 2]);
                    }
                }
            }
            return Convert.ToString(latestDate);
        }

        static string LatestDate11(IList<string> goalsList) // До выполнения самой поздней цели
        {
            int latestDate = 0;
            string goalTitle = "";
            for (int i = 0; i < goalsList.Count; i++)
            {
                if (i % 4 == 2)
                {
                    if (Convert.ToInt32(goalsList[i]) > latestDate)
                    {
                        latestDate = Convert.ToInt32(goalsList[i]);
                        goalTitle = Convert.ToString(goalsList[i - 2]);
                    }
                }
            }
            return goalTitle;
        }

        static string EarliestDate1(IList<string> goalsList) // До выполнения самой ранней цели
        {
            int earliestDate = 1000000000;
            string goalTitle = "";
            for (int i = 0; i < goalsList.Count; i++)
            {
                if (i % 4 == 2)
                {
                    if (Convert.ToInt32(goalsList[i]) < earliestDate && Convert.ToInt32(goalsList[i]) != 0)
                    {
                        earliestDate = Convert.ToInt32(goalsList[i]);
                        goalTitle = Convert.ToString(goalsList[i - 2]);
                    }
                }
            }
            return Convert.ToString(earliestDate);
        }
        static string EarliestDate11(IList<string> goalsList) // До выполнения самой ранней цели
        {
            int earliestDate = 1000000000;
            string goalTitle = "";
            for (int i = 0; i < goalsList.Count; i++)
            {
                if (i % 4 == 2)
                {
                    if (Convert.ToInt32(goalsList[i]) < earliestDate && Convert.ToInt32(goalsList[i]) != 0)
                    {
                        earliestDate = Convert.ToInt32(goalsList[i]);
                        goalTitle = Convert.ToString(goalsList[i - 2]);
                    }
                }
            }
            return goalTitle;
        }
    }
}