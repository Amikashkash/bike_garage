import{j as e,c as E,r as d}from"./client.CZIp3qzo.js";import"./react-vendor.CiW5Bwbg.js";const T=({repair:s,onCategoryClick:i})=>e.jsxs("div",{className:"bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl overflow-hidden h-fit",children:[e.jsx("div",{className:"bg-blue-500/20 px-4 py-3 border-b border-blue-500/30",children:e.jsxs("h3",{className:"text-lg font-bold text-white flex items-center gap-2",children:[e.jsx("i",{className:"fas fa-info-circle text-blue-400"}),"פרטי התיקון"]})}),e.jsxs("div",{className:"p-4 space-y-3",children:[e.jsxs("div",{className:"flex items-center gap-3 p-3 bg-slate-700/50 border border-slate-600 rounded-lg",children:[e.jsx("div",{className:"w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center",children:e.jsx("i",{className:"fas fa-bicycle text-white"})}),e.jsxs("div",{className:"flex-1 min-w-0",children:[e.jsxs("h4",{className:"font-bold text-white text-base truncate",children:[s.bike.brand," ",s.bike.model]}),e.jsx("p",{className:"text-slate-300 text-sm truncate",children:s.customer.name})]})]}),e.jsxs("div",{className:"space-y-2 text-sm",children:[e.jsxs("div",{className:"flex items-center justify-between",children:[e.jsx("span",{className:"text-slate-300",children:"טלפון:"}),e.jsx("span",{className:"text-white font-medium",children:s.customer.phone||"לא צוין"})]}),e.jsxs("div",{className:"flex items-center justify-between",children:[e.jsx("span",{className:"text-slate-300",children:"תאריך:"}),e.jsx("span",{className:"text-white font-medium",children:s.created_at})]})]}),s.subcategories&&s.subcategories.length>0&&e.jsxs("div",{children:[e.jsxs("h6",{className:"text-white font-medium mb-2 flex items-center gap-2 text-sm",children:[e.jsx("i",{className:"fas fa-tags text-yellow-400"}),"קטגוריות התקלה"]}),e.jsx("div",{className:"space-y-1",children:s.subcategories.map(a=>e.jsx("div",{onClick:()=>i(a.name),className:"bg-yellow-500/10 border border-yellow-400/30 rounded-lg p-2 cursor-pointer transition-all hover:bg-yellow-500/20",title:"לחץ להוספה לתיאור הפעולה",children:e.jsxs("div",{className:"flex items-center justify-between",children:[e.jsxs("div",{className:"flex items-center gap-2 min-w-0 flex-1",children:[e.jsx("i",{className:"fas fa-tag text-yellow-400 text-xs flex-shrink-0"}),e.jsx("span",{className:"text-yellow-100 font-medium text-sm truncate",children:a.name})]}),e.jsx("i",{className:"fas fa-plus-circle text-yellow-400 text-xs flex-shrink-0"})]})},a.id))})]}),s.problem_description&&e.jsxs("div",{children:[e.jsxs("h6",{className:"text-white font-medium mb-2 flex items-center gap-2 text-sm",children:[e.jsx("i",{className:"fas fa-exclamation-triangle text-red-400"}),"תיאור התקלה"]}),e.jsx("div",{className:"bg-red-500/10 border border-red-400/30 rounded-lg p-3",children:e.jsx("p",{className:"text-red-100 text-sm",children:s.problem_description})})]})]})]}),P=({items:s,totalPrice:i})=>!s||s.length===0?null:e.jsxs("div",{className:"mb-4",children:[e.jsxs("h6",{className:"text-white font-medium mb-3 flex items-center gap-2 text-sm",children:[e.jsx("i",{className:"fas fa-list text-blue-400"}),"פעולות תיקון קיימות"]}),e.jsx("div",{className:"grid grid-cols-1 gap-3 mb-4",children:s.map(a=>e.jsx("div",{className:"bg-slate-700/50 border border-slate-600 rounded-lg p-3",children:e.jsxs("div",{className:"flex flex-col sm:flex-row sm:items-center justify-between gap-2",children:[e.jsxs("div",{className:"flex items-center gap-2 flex-1 min-w-0",children:[e.jsx("div",{className:"w-6 h-6 bg-blue-500/20 rounded flex items-center justify-center flex-shrink-0",children:e.jsx("i",{className:"fas fa-wrench text-blue-400 text-xs"})}),e.jsx("span",{className:"text-white font-medium text-sm break-words",children:a.description})]}),e.jsxs("div",{className:"flex items-center justify-between sm:justify-end gap-2",children:[e.jsxs("span",{className:"text-white font-bold text-sm",children:["₪",a.price]}),a.is_approved?e.jsxs("span",{className:"bg-green-500/20 text-green-300 px-2 py-1 rounded text-xs font-medium whitespace-nowrap",children:[e.jsx("i",{className:"fas fa-check mr-1"}),"אושר"]}):e.jsxs("span",{className:"bg-orange-500/20 text-orange-300 px-2 py-1 rounded text-xs font-medium whitespace-nowrap",children:[e.jsx("i",{className:"fas fa-clock mr-1"}),"ממתין"]})]})]})},a.id))}),e.jsx("div",{className:"bg-slate-700/30 border border-slate-600 rounded-lg p-3 mb-4",children:e.jsxs("div",{className:"flex items-center justify-between",children:[e.jsx("span",{className:"text-slate-300 font-medium text-sm",children:'סה"כ קיים:'}),e.jsxs("span",{className:"text-white font-bold text-lg",children:["₪",i.toFixed(2)]})]})}),e.jsx("div",{className:"border-t border-slate-600 pt-4",children:e.jsxs("h6",{className:"text-white font-medium flex items-center gap-2 text-sm",children:[e.jsx("i",{className:"fas fa-plus text-green-400"}),"הוסף פעולות נוספות"]})})]}),D=({index:s,item:i,onUpdate:a,onRemove:t,showRemove:m})=>e.jsx("div",{className:"repair-item-row",children:e.jsxs("div",{className:"flex flex-col sm:flex-row gap-3 items-stretch sm:items-center",children:[e.jsx("div",{className:"flex-1 min-w-0",children:e.jsx("input",{type:"text",value:i.description,onChange:x=>a(s,"description",x.target.value),className:"w-full px-3 py-2 bg-slate-700/50 border border-slate-600 rounded-lg text-white placeholder-slate-400 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent",placeholder:"תיאור הפעולה (לדוגמה: החלפת בלמים קדמיים)",required:!0})}),e.jsxs("div",{className:"flex gap-3 items-center",children:[e.jsx("div",{className:"w-32 flex-shrink-0",children:e.jsx("input",{type:"number",value:i.price,onChange:x=>a(s,"price",x.target.value),className:"w-full px-3 py-2 bg-slate-700/50 border border-slate-600 rounded-lg text-white placeholder-slate-400 text-sm focus:ring-2 focus:ring-green-500 focus:border-transparent",placeholder:"מחיר (₪)",step:"10",min:"0",required:!0})}),e.jsx("div",{className:"w-10 flex-shrink-0 flex justify-center",children:m&&e.jsx("button",{type:"button",onClick:()=>t(s),className:"w-8 h-8 bg-red-500/20 hover:bg-red-500/30 text-red-400 rounded-lg border border-red-400/40 hover:border-red-400/60 transition-all duration-200 flex items-center justify-center",title:"הסר פעולה",children:e.jsx("i",{className:"fas fa-trash text-xs"})})})]})]})}),H=({sendNotification:s,onToggle:i,customer:a,bike:t})=>e.jsxs("div",{className:"bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6 mt-6",children:[e.jsxs("h3",{className:"text-lg font-bold text-white mb-4 flex items-center gap-2",children:[e.jsx("i",{className:"fas fa-bell text-blue-400"}),"התראות ללקוח"]}),e.jsxs("div",{className:"space-y-4",children:[e.jsxs("div",{className:"flex items-start gap-3 p-3 bg-slate-700/30 rounded-lg",children:[e.jsx("div",{className:"flex-shrink-0 mt-1",children:e.jsx("input",{type:"checkbox",id:"send-notification",checked:s,onChange:m=>i(m.target.checked),className:"w-5 h-5 text-blue-500 bg-slate-600 border-slate-500 rounded focus:ring-blue-500 focus:ring-2"})}),e.jsxs("label",{htmlFor:"send-notification",className:"flex-1 cursor-pointer",children:[e.jsx("div",{className:"text-white font-medium mb-1",children:"📱 שלח התראה ללקוח"}),e.jsx("div",{className:"text-slate-400 text-sm",children:"הלקוח יקבל התראת דחיפה ואימייל עם בקשה לאישור הפעולות"})]})]}),s&&e.jsx("div",{className:"bg-blue-500/10 border border-blue-400/30 rounded-lg p-3",children:e.jsxs("div",{className:"flex items-start gap-3",children:[e.jsx("i",{className:"fas fa-mobile-alt text-blue-400 text-lg mt-1"}),e.jsxs("div",{className:"flex-1",children:[e.jsx("div",{className:"text-blue-200 font-medium text-sm mb-1",children:"תצוגה מקדימה של ההתראה:"}),e.jsxs("div",{className:"text-blue-100 text-sm",children:['"נדרש אישור - תיקון ',t.brand," ",t.model,'"',e.jsx("br",{}),e.jsxs("span",{className:"text-blue-300",children:["האבחון לתיקון האופניים ",t.brand," ",t.model," מוכן. יש צורך באישור שלך לפעולות התיקון."]})]})]})]})}),e.jsxs("div",{className:"flex flex-wrap items-center gap-3 text-sm",children:[e.jsxs("div",{className:"flex items-center gap-2 text-slate-400",children:[e.jsx("i",{className:"fas fa-user"}),e.jsx("span",{children:a.name})]}),a.phone&&e.jsxs("div",{className:"flex items-center gap-2 text-slate-400",children:[e.jsx("i",{className:"fas fa-phone"}),e.jsx("span",{children:a.phone})]}),a.email?e.jsxs("div",{className:"flex items-center gap-2 text-slate-400",children:[e.jsx("i",{className:"fas fa-envelope"}),e.jsx("span",{children:a.email})]}):e.jsxs("div",{className:"flex items-center gap-2 text-yellow-400",children:[e.jsx("i",{className:"fas fa-exclamation-triangle"}),e.jsx("span",{className:"text-sm",children:"אין אימייל - רק התראת דחיפה"})]})]})]})]}),q=({repairId:s})=>{const[i,a]=d.useState(!0),[t,m]=d.useState(null),[x,p]=d.useState(""),[u,j]=d.useState(""),[o,b]=d.useState([{description:"",price:""}]),[N,k]=d.useState(!0),[v,g]=d.useState(!1),[h,_]=d.useState(0);d.useEffect(()=>{R()},[s]);const R=async()=>{try{const r=await fetch(`/api/repair/${s}/diagnosis/`,{credentials:"same-origin"});if(!r.ok)throw new Error("Failed to load repair data");const l=await r.json();m(l),j(l.diagnosis||""),a(!1)}catch(r){p(r.message),a(!1)}},w=(r,l,n)=>{const c=[...o];c[r][l]=n,b(c)},S=()=>{b([...o,{description:"",price:""}])},F=r=>{const l=o.filter((n,c)=>c!==r);b(l)},I=r=>{const l=o.findIndex(n=>!n.description.trim());l>=0?w(l,"description",r):b([...o,{description:r,price:""}])};d.useEffect(()=>{const r=o.reduce((l,n)=>{const c=parseFloat(n.price)||0;return l+c},0);_(r)},[o]);const C=async r=>{r.preventDefault();const l=o.filter(n=>n.description.trim()&&n.price&&parseFloat(n.price)>0);if(l.length===0){p("נא להוסיף לפחות פעולת תיקון אחת עם מחיר");return}g(!0),p("");try{const c=await(await fetch(`/api/repair/${s}/diagnosis/submit/`,{method:"POST",headers:{"Content-Type":"application/json","X-CSRFToken":document.querySelector("[name=csrfmiddlewaretoken]").value},credentials:"same-origin",body:JSON.stringify({diagnosis:u,repair_items:l.map(y=>({description:y.description.trim(),price:parseFloat(y.price)})),send_notification:N})})).json();c.success?window.location.href="/manager/dashboard/":(p(c.error||"שגיאה בשמירת האבחון"),g(!1))}catch{p("שגיאה בשמירת האבחון"),g(!1)}};return i?e.jsx("div",{className:"min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center",children:e.jsxs("div",{className:"text-center",children:[e.jsx("div",{className:"w-16 h-16 border-4 border-blue-400 border-t-transparent rounded-full animate-spin mx-auto mb-4"}),e.jsx("p",{className:"text-slate-300 text-lg",children:"טוען נתונים..."})]})}):x&&!t?e.jsx("div",{className:"min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center",children:e.jsx("div",{className:"bg-red-900/20 border border-red-500/30 rounded-2xl p-8 max-w-md mx-auto",children:e.jsxs("div",{className:"text-center",children:[e.jsx("i",{className:"fas fa-exclamation-triangle text-red-400 text-4xl mb-4"}),e.jsx("h2",{className:"text-xl font-bold text-white mb-2",children:"שגיאה"}),e.jsx("p",{className:"text-red-200 mb-4",children:x}),e.jsx("a",{href:"/manager/dashboard/",className:"bg-red-500/20 hover:bg-red-500/30 text-red-300 px-4 py-2 rounded-lg border border-red-400/40 transition-all duration-200 inline-block",children:"חזור לדשבורד"})]})})}):e.jsxs(e.Fragment,{children:[e.jsx("style",{children:`
        @media print {
          /* Hide EVERYTHING except the diagnosis content */
          body > *:not(#root) {
            display: none !important;
          }

          header, footer, nav, aside {
            display: none !important;
          }

          /* Hide buttons and interactive elements */
          button, input[type="button"], input[type="submit"],
          a[href*="dashboard"], .notification-settings {
            display: none !important;
          }

          /* Optimize page for print */
          * {
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
          }

          body {
            background: white !important;
            color: black !important;
            margin: 0 !important;
            padding: 20px !important;
          }

          #root {
            background: white !important;
          }

          .min-h-screen {
            min-height: auto !important;
            background: white !important;
          }

          .bg-gradient-to-br {
            background: white !important;
          }

          /* Reset all backgrounds to white */
          .bg-slate-800\\/50, .bg-slate-700\\/50, .bg-slate-700\\/30,
          .bg-slate-600, .bg-slate-800, .bg-slate-900,
          .bg-blue-500\\/20, .bg-green-500\\/20, .bg-orange-500\\/20,
          .bg-red-500\\/10, .bg-yellow-500\\/10, .bg-blue-900\\/30 {
            background: white !important;
          }

          /* Make all borders visible */
          .bg-slate-800\\/50, .bg-slate-700\\/50, .border {
            border: 1px solid #333 !important;
          }

          /* Text colors - all to black */
          .text-white, .text-slate-300, .text-slate-200, .text-slate-100,
          .text-blue-300, .text-red-100, .text-yellow-100, .text-orange-200,
          .text-green-300, .text-green-200, .text-slate-400 {
            color: black !important;
          }

          /* Headers stay bold */
          .text-green-400, .text-orange-400, .text-blue-400,
          .text-red-400, .text-yellow-400 {
            color: #000 !important;
            font-weight: bold !important;
          }

          /* Icons */
          i, .fas, .far {
            color: #666 !important;
          }

          /* Layout */
          .max-w-7xl {
            max-width: 100% !important;
            padding: 0 20px !important;
          }

          .px-4, .px-6, .px-8, .py-8 {
            padding-left: 10px !important;
            padding-right: 10px !important;
          }

          /* Flex to block */
          .flex.flex-col.xl\\:flex-row {
            display: block !important;
          }

          .xl\\:w-96 {
            width: 100% !important;
            margin-bottom: 15px !important;
          }

          .flex-1 {
            width: 100% !important;
          }

          /* Remove effects */
          * {
            box-shadow: none !important;
            text-shadow: none !important;
            backdrop-filter: none !important;
          }

          /* Page breaks */
          .print-section {
            page-break-inside: avoid;
            margin-bottom: 15px !important;
            padding: 10px !important;
          }

          /* Typography */
          h1 {
            font-size: 24px !important;
            color: black !important;
            margin-bottom: 5px !important;
            background: none !important;
            -webkit-background-clip: unset !important;
            background-clip: unset !important;
            -webkit-text-fill-color: black !important;
          }

          h2, h3, h4 {
            color: black !important;
            margin-top: 10px !important;
            margin-bottom: 5px !important;
          }

          p {
            color: black !important;
            line-height: 1.4 !important;
          }

          /* Show hidden print elements */
          .hidden.print\\:block {
            display: block !important;
          }

          /* Total price box */
          .total-price {
            background: #f5f5f5 !important;
            border: 2px solid #000 !important;
            padding: 15px !important;
            margin-top: 20px !important;
          }

          /* Clean textarea for print */
          textarea {
            border: 1px solid #ccc !important;
            background: white !important;
            color: black !important;
            font-family: inherit !important;
            padding: 10px !important;
            width: 100% !important;
          }

          /* Rounded corners off */
          .rounded-xl, .rounded-lg {
            border-radius: 0 !important;
          }

          /* Grid stays as is */
          .grid {
            display: block !important;
          }

          .space-y-3 > * + *,
          .space-y-2 > * + * {
            margin-top: 10px !important;
          }
        }
      `}),e.jsx("div",{className:"min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900",children:e.jsxs("div",{className:"max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8",children:[e.jsx("div",{className:"text-center mb-8",children:e.jsxs("div",{className:"flex flex-col lg:flex-row lg:items-center lg:justify-between",children:[e.jsxs("div",{className:"mb-4 lg:mb-0",children:[e.jsxs("h1",{className:"text-3xl lg:text-4xl font-bold mb-2 bg-gradient-to-r from-blue-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent",children:["🔍 אבחון תיקון #",t.id]}),e.jsx("p",{className:"text-slate-300 text-base",children:t.is_editing?"עריכת אבחון והצעת מחיר מפורטת":"אבחון מקצועי והצעת מחיר מדויקת"})]}),e.jsx("div",{className:"hidden sm:flex justify-center lg:justify-end",children:e.jsx("div",{className:"bg-blue-500/20 border border-blue-400/40 rounded-xl px-4 py-2",children:e.jsxs("nav",{className:"flex items-center gap-2 text-sm",children:[e.jsxs("a",{href:"/manager/dashboard/",className:"text-blue-300 hover:text-blue-200 transition-colors",children:[e.jsx("i",{className:"fas fa-tachometer-alt mr-1"}),"דשבורד מנהל"]}),e.jsx("i",{className:"fas fa-chevron-left text-slate-400"}),e.jsxs("span",{className:"text-white font-medium",children:[e.jsx("i",{className:"fas fa-stethoscope mr-1"}),t.is_editing?"עריכת אבחון":"אבחון"]})]})})})]})}),(!t.existing_items||t.existing_items.length===0)&&e.jsx("div",{className:"mb-6",children:e.jsx("div",{className:"bg-blue-900/30 border border-blue-500/40 rounded-xl overflow-hidden backdrop-blur-sm",children:e.jsx("div",{className:"px-4 py-3 bg-blue-500/20 border-b border-blue-500/30",children:e.jsxs("div",{className:"flex items-center gap-3",children:[e.jsx("div",{className:"w-8 h-8 bg-blue-500/30 rounded-lg flex items-center justify-center",children:e.jsx("i",{className:"fas fa-lightbulb text-blue-400"})}),e.jsxs("div",{children:[e.jsx("h3",{className:"text-lg font-bold text-white",children:"💡 הוראות לאבחון מדויק"}),e.jsx("p",{className:"text-blue-200 text-sm",children:"הוסף את כל הפעולות הנדרשות עם מחירים מדויקים, וכך הלקוח יוכל לאשר בדיוק איזה פעולות הוא רוצה לבצע."})]})]})})})}),x&&e.jsx("div",{className:"mb-6 p-4 bg-red-500/10 border border-red-400/30 rounded-xl",children:e.jsxs("div",{className:"flex items-center gap-2 text-red-300",children:[e.jsx("i",{className:"fas fa-exclamation-triangle"}),e.jsx("span",{children:x})]})}),e.jsxs("div",{className:"flex flex-col xl:flex-row gap-6 w-full",children:[e.jsx("div",{className:"w-full xl:w-96 xl:shrink-0 order-1 xl:order-1 print-section",children:e.jsx(T,{repair:t,onCategoryClick:I})}),e.jsx("div",{className:"flex-1 min-w-0 order-2 xl:order-2",children:e.jsxs("form",{onSubmit:C,children:[e.jsxs("div",{className:"grid grid-cols-1 gap-6",children:[e.jsxs("div",{className:"bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl overflow-hidden h-fit print-section",children:[e.jsx("div",{className:"bg-green-500/20 px-4 py-3 border-b border-green-500/30",children:e.jsxs("h3",{className:"text-lg font-bold text-white flex items-center gap-2",children:[e.jsx("i",{className:"fas fa-stethoscope text-green-400"}),"אבחון והצעת מחיר"]})}),e.jsxs("div",{className:"p-4",children:[e.jsxs("label",{className:"block text-slate-300 text-sm font-medium mb-2",children:[e.jsx("i",{className:"fas fa-clipboard-list text-blue-400 mr-2"}),"אבחון (אופציונלי)"]}),e.jsx("textarea",{value:u,onChange:r=>j(r.target.value),className:"w-full px-4 py-3 bg-slate-700/50 border border-slate-600 rounded-lg text-white placeholder-slate-400 text-base focus:ring-2 focus:ring-green-500 focus:border-transparent resize-vertical min-h-[200px]",placeholder:"פרט את האבחון..."})]})]}),e.jsxs("div",{className:"bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl overflow-hidden print-section",children:[e.jsxs("div",{className:"bg-orange-500/20 px-4 py-3 border-b border-orange-500/30",children:[e.jsxs("h3",{className:"text-lg font-bold text-white flex items-center gap-2",children:[e.jsx("i",{className:"fas fa-tools text-orange-400"}),"פעולות תיקון ומחירים"]}),e.jsx("p",{className:"text-orange-200 text-sm mt-1",children:"הוסף את כל הפעולות הנדרשות עם מחירים מדויקים"})]}),e.jsxs("div",{className:"p-4",children:[e.jsx(P,{items:t.existing_items,totalPrice:t.total_existing_price}),e.jsx("div",{className:"space-y-3",children:o.map((r,l)=>e.jsx(D,{index:l,item:r,onUpdate:w,onRemove:F,showRemove:o.length>1},l))}),e.jsxs("div",{className:"flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 mt-4",children:[e.jsxs("button",{type:"button",onClick:S,className:"bg-green-500/20 hover:bg-green-500/30 text-green-300 px-4 py-2 rounded-lg border border-green-400/40 hover:border-green-400/60 transition-all duration-200 flex items-center justify-center gap-2",children:[e.jsx("i",{className:"fas fa-plus"}),e.jsx("span",{className:"text-sm font-medium",children:"הוסף פעולה נוספת"})]}),e.jsxs("div",{className:"bg-green-500/10 border border-green-400/30 rounded-lg px-4 py-2 text-center sm:text-right",children:[e.jsx("span",{className:"text-green-300 font-medium text-sm",children:'סה"כ פעולות חדשות: '}),e.jsxs("span",{className:"text-green-200 font-bold text-base",children:["₪",h.toFixed(2)]})]})]})]})]}),e.jsx("div",{className:"hidden print:block total-price bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl overflow-hidden",children:e.jsxs("div",{className:"p-6",children:[e.jsx("h3",{className:"text-2xl font-bold text-center mb-4",children:"סיכום מחיר"}),e.jsxs("div",{className:"space-y-2 text-lg",children:[t.existing_items&&t.existing_items.length>0&&e.jsxs("div",{className:"flex justify-between",children:[e.jsx("span",{children:"פעולות קיימות:"}),e.jsxs("span",{className:"font-bold",children:["₪",t.total_existing_price.toFixed(2)]})]}),h>0&&e.jsxs("div",{className:"flex justify-between",children:[e.jsx("span",{children:"פעולות חדשות:"}),e.jsxs("span",{className:"font-bold",children:["₪",h.toFixed(2)]})]}),e.jsx("div",{className:"border-t-2 border-black pt-2 mt-2",children:e.jsxs("div",{className:"flex justify-between text-xl font-bold",children:[e.jsx("span",{children:'סה"כ:'}),e.jsxs("span",{children:["₪",(t.total_existing_price+h).toFixed(2)]})]})})]})]})})]}),e.jsx(H,{sendNotification:N,onToggle:k,customer:t.customer,bike:t.bike}),e.jsxs("div",{className:"flex flex-col gap-4 mt-6",children:[e.jsxs("button",{type:"button",onClick:()=>window.print(),className:"bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-semibold py-4 px-8 rounded-xl transition-all shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95",children:[e.jsx("i",{className:"fas fa-print mr-2"}),"הדפס / שמור כ-PDF"]}),e.jsx("button",{type:"submit",disabled:v,className:"bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white font-semibold py-4 px-8 rounded-xl transition-all shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none",children:v?e.jsxs(e.Fragment,{children:[e.jsx("i",{className:"fas fa-spinner fa-spin mr-2"}),"שומר..."]}):t.is_editing?e.jsxs(e.Fragment,{children:[e.jsx("i",{className:"fas fa-save mr-2"}),"עדכן אבחון ושלח ללקוח"]}):e.jsxs(e.Fragment,{children:[e.jsx("i",{className:"fas fa-check mr-2"}),"שמור אבחון ושלח ללקוח"]})}),e.jsxs("a",{href:"/manager/dashboard/",className:"bg-slate-600/50 hover:bg-slate-600/70 text-slate-200 font-semibold py-4 px-8 rounded-xl transition-all text-center border border-slate-500/30 hover:border-slate-400/50",children:[e.jsx("i",{className:"fas fa-times mr-2"}),"ביטול"]})]})]})})]})]})})]})},f=document.getElementById("root");if(f){const s=E.createRoot(f),i=f.dataset.repairId?parseInt(f.dataset.repairId):null;s.render(e.jsx(q,{repairId:i}))}
//# sourceMappingURL=repair-diagnosis.js.map
