using Android.App;
using Android.Content;
using Android.OS;
using Android.Runtime;
using Android.Views;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Android.Content.PM;
using AndroidX.AppCompat.App;
using Android.Widget;
using AndroidX.RecyclerView.Widget;

namespace ProjectCurs
{
    [Activity(Label = "Цель",  ConfigurationChanges = ConfigChanges.ScreenSize | ConfigChanges.Orientation, ScreenOrientation = ScreenOrientation.Locked)]
    [Obsolete]
    public class Goal : AppCompatActivity
    {
        static public IList<string> stringsinput = new List<string>();
        static public IList<string> achievelist = new List<string>() { "false", "" };
        TextView goalText;
        TextView dateTextInput;
        TextView difficultTextInput;
        protected override void OnCreate(Bundle savedInstanceState)
        {
            base.OnCreate(savedInstanceState);
            SetContentView(Resource.Layout.GoalOne);
            if (Intent.GetStringArrayListExtra("stringsinput") != null)
                stringsinput = Intent.Extras.GetStringArrayList("stringsinput");
            if (Intent.GetStringArrayListExtra("achievelist") != null && Intent.GetStringArrayListExtra("achievelist").Count != 0)
                achievelist = Intent.Extras.GetStringArrayList("achievelist");
            string data = Intent.GetStringExtra("Data");
            string point = Intent.GetStringExtra("Point");
            string goal = Intent.GetStringExtra("Goal");
            string fromMain = Intent.GetStringExtra("fromMain");
            int count = Intent.GetIntExtra("index", -1);
            goalText = FindViewById<TextView>(Resource.Id.GoalText);
            dateTextInput = FindViewById<TextView>(Resource.Id.DateTextInput);
            difficultTextInput = FindViewById<TextView>(Resource.Id.DifficultTextInput);
            TextView howMuchDayRemain = FindViewById<TextView>(Resource.Id.HowMuchDaysRemain2);
            if (data != null && point != null && goal != null || count != -1)
            {
                if (count == -1)
                {
                    goalText.Text = goal;
                    dateTextInput.Text = data;
                    difficultTextInput.Text = point;
                    DateTime now = DateTime.Now;
                    DateTime choose = new DateTime(int.Parse(data.Substring(6, 4)), int.Parse(data.Substring(3, 2)), int.Parse(data.Substring(0, 2)));
                    int data1 = (choose - now).Days + 1;
                    howMuchDayRemain.Text = data1.ToString();

                    stringsinput.Add(goal);
                    stringsinput.Add(data);
                    stringsinput.Add(data1.ToString());
                    stringsinput.Add(point);
                }
                else
                {
                    goalText.Text = stringsinput[count*4];
                    dateTextInput.Text = stringsinput[count*4+1];
                    howMuchDayRemain.Text = stringsinput[count * 4 + 2];
                    difficultTextInput.Text = stringsinput[count*4+3];
                }
            }
            CheckBox oneCheck = FindViewById<CheckBox>(Resource.Id.appCompatCheckBox1);
            CheckBox secondCheck = FindViewById<CheckBox>(Resource.Id.appCompatCheckBox2);
            EditText inputtext = FindViewById<EditText>(Resource.Id.ChooseDays);
            inputtext.Enabled = false;
            oneCheck.Click += (o, e) =>
            {
                if (oneCheck.Checked)
                {
                    if (secondCheck.Checked)
                    {
                        oneCheck.Clickable = true;
                        oneCheck.Focusable = true;
                        secondCheck.Clickable = true;
                        secondCheck.Focusable = true;
                        //inputtext.Enabled = true;
                    }
                    else
                    {
                        secondCheck.Clickable = false;
                        secondCheck.Focusable = false;
                        //inputtext.Enabled = false;
                    }
                }
                else if (!oneCheck.Checked)
                {
                    if (secondCheck.Checked)
                    {
                        oneCheck.Clickable = false;
                        oneCheck.Focusable = false;
                    }
                    secondCheck.Clickable = true;
                    secondCheck.Focusable = true;
                }
            };
            secondCheck.Click += (o, e) =>
            {
                if (secondCheck.Checked)
                {
                    inputtext.Enabled = true;
                    if (oneCheck.Checked)
                    {
                        oneCheck.Clickable = true;
                        oneCheck.Focusable = true;
                    }
                    else
                    {
                        oneCheck.Clickable = false;
                        oneCheck.Focusable = false;
                    }
                }
                else if (!secondCheck.Checked)
                {
                    inputtext.Enabled = false;
                    if (inputtext != null)
                        inputtext.Text = "";
                    if (oneCheck.Checked)
                    {
                        secondCheck.Clickable = false;
                        secondCheck.Focusable = false;
                    }
                    oneCheck.Clickable = true;
                    oneCheck.Focusable = true;
                }
            };
            //Добавить сюда кнопку, по которой на главное меню переходишь
            Button continuegoal = FindViewById<Button>(Resource.Id.buttonContinueGoal);
            continuegoal.Click += (o, e) =>
            {
                if (oneCheck.Checked && secondCheck.Checked)
                    Toast.MakeText(this, $"Можно выбрать только одну галочку!", ToastLength.Long).Show();
                else if (secondCheck.Checked && inputtext.Text.Length == 0)
                    Toast.MakeText(this, $"Нужно ввести кол-во дней", ToastLength.Long).Show();
                else if (secondCheck.Checked && int.Parse(inputtext.Text) <= 0)
                    Toast.MakeText(this, $"Кол-во дней должно быть больше 0", ToastLength.Long).Show();
                else if (oneCheck.Checked && fromMain == null)
                {
                    stringsinput[stringsinput.Count - 2] = (int.Parse(stringsinput[stringsinput.Count - 2]) - 1).ToString();
                    var intent = new Intent(this, typeof(MainActivity));
                    if (Int32.Parse(stringsinput[stringsinput.Count - 2]) <= 0)
                        if (achievelist[1] != "")
                            achievelist[1] = (int.Parse(achievelist[1]) + int.Parse(difficultTextInput.Text)).ToString();
                        else
                            achievelist[1] = int.Parse(difficultTextInput.Text).ToString();
                    intent.PutStringArrayListExtra("achievelist", achievelist);
                    intent.PutStringArrayListExtra("stringsinput", stringsinput);
                    StartActivity(intent);
                }
                else if (secondCheck.Checked && fromMain == null)
                {
                    stringsinput[stringsinput.Count - 2] = (int.Parse(stringsinput[stringsinput.Count - 2]) - int.Parse(inputtext.Text)).ToString();
                    var intent = new Intent(this, typeof(MainActivity));
                    if (Int32.Parse(stringsinput[stringsinput.Count - 2]) <= 0)
                        if (achievelist[1] != "")
                            achievelist[1] = (int.Parse(achievelist[1]) + int.Parse(difficultTextInput.Text)).ToString();
                        else
                            achievelist[1] = int.Parse(difficultTextInput.Text).ToString();
                    intent.PutStringArrayListExtra("achievelist", achievelist);
                    intent.PutStringArrayListExtra("stringsinput", stringsinput);
                    StartActivity(intent);
                }
                else if (oneCheck.Checked && fromMain != null)
                {
                    stringsinput[count*4 + 2] = (int.Parse(stringsinput[count*4 + 2]) - 1).ToString();
                    var intent = new Intent(this, typeof(MainActivity));
                    if (Int32.Parse(stringsinput[count*4+2]) <= 0)
                    {
                        if (achievelist[1] != "")
                            achievelist[1] = (int.Parse(achievelist[1]) + int.Parse(difficultTextInput.Text)).ToString();
                        else
                            achievelist[1] = int.Parse(difficultTextInput.Text).ToString();
                    }
                    intent.PutStringArrayListExtra("achievelist", achievelist);
                    intent.PutStringArrayListExtra("stringsinput", stringsinput);
                    StartActivity(intent);
                }
                else if (secondCheck.Checked && fromMain != null)
                {
                    stringsinput[count*4 + 2] = (int.Parse(stringsinput[count*4 + 2]) - int.Parse(inputtext.Text)).ToString();
                    var intent = new Intent(this, typeof(MainActivity));
                    if (Int32.Parse(stringsinput[count * 4 + 2]) <= 0)
                    {
                        if (achievelist[1] != "")
                            achievelist[1] = (int.Parse(achievelist[1]) + int.Parse(difficultTextInput.Text)).ToString();
                        else
                            achievelist[1] = int.Parse(difficultTextInput.Text).ToString();
                    }
                    intent.PutStringArrayListExtra("achievelist", achievelist);
                    intent.PutStringArrayListExtra("stringsinput", stringsinput);
                    StartActivity(intent);
                }
                else
                {
                    var intent = new Intent(this, typeof(MainActivity));
                    intent.PutStringArrayListExtra("stringsinput", stringsinput);
                    intent.PutStringArrayListExtra("achievelist", achievelist);
                    StartActivity(intent);
                }
            };
            Button delgoal = FindViewById<Button>(Resource.Id.DelGoalButton1);
            delgoal.Click += (o, e) =>
            {
                for (int i = 0; i < 4; i++)
                {
                    if (count == -1)
                        stringsinput.RemoveAt(stringsinput.Count - 1);
                    else
                        stringsinput.RemoveAt(count * 4);
                }
                var intent = new Intent(this, typeof(MainActivity));
                intent.PutStringArrayListExtra("stringsinput", stringsinput);
                intent.PutStringArrayListExtra("achievelist", achievelist);
                Toast.MakeText(this, "Удаление произведено", ToastLength.Long).Show();
                StartActivity(intent);
            };
        }
    }
}