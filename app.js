document.addEventListener('DOMContentLoaded', () => {
    const API_URL = 'http://127.0.0.1:5000';

    // --- عناصر الواجهة (DOM Elements) ---
    const phoneGrid = document.getElementById('phone-grid');
    const searchInput = document.getElementById('search-input');
    const brandsContainer = document.getElementById('brand-filters-container');
    const clearComparisonBtn = document.querySelector('.clear-comparison');
    
    // عناصر النافذة المنبثقة (Modal)
    const modalOverlay = document.getElementById('comparison-modal-overlay');
    const modalCloseBtn = document.getElementById('modal-close-btn');
    const modalLoader = document.getElementById('modal-loader');
    const comparisonTableBody = document.getElementById('comparison-table-body');
    const comparisonTableHeader = document.getElementById('comparison-table-header');

    // عناصر الشات بوت (الجديدة)
    const chatbotToggler = document.getElementById('chatbot-toggler');
    const closeChatBtn = document.getElementById('close-chat');
    const chatContainer = document.querySelector('.chatbot-container');
    const chatInput = document.getElementById("chat-input");
    const chatSend = document.getElementById("chat-send");
    const chatMessages = document.getElementById("chat-messages");

    // متغيرات الحالة
    let allPhonesData = [];
    let comparisonList = [];

    // --- التشغيل المبدئي ---
    init();

    async function init() {
        await loadSidebarBrands(); // تحميل الشركات والأيقونات
        await loadPhones();        // تحميل الهواتف
        setupEvents();             // تفعيل الأزرار والبحث
    }

    // --- 1. تحميل القائمة الجانبية مع الأيقونات ---
    async function loadSidebarBrands() {
        try {
            const res = await fetch(`${API_URL}/api/brands`);
            if (!res.ok) throw new Error('Failed to load brands');
            const brands = await res.json();

            // خريطة الأيقونات (Mapping)
            const brandIcons = {
                'Apple': 'fa-brands fa-apple',
                'Samsung': 'fa-brands fa-android',
                'Google': 'fa-brands fa-google',
                'Huawei': 'fa-solid fa-mobile-screen',
                'Xiaomi': 'fa-solid fa-m',
                'Oppo': 'fa-solid fa-o',
                'Realme': 'fa-solid fa-r',
                'Sony': 'fa-solid fa-tv', // أو أيقونة أخرى
                'Honor': 'fa-solid fa-h',
                'Infinix': 'fa-solid fa-i',
                'Tecno': 'fa-solid fa-t',
                'Motorola': 'fa-solid fa-m',
                'Vivo': 'fa-solid fa-v',
                'default': 'fa-solid fa-mobile-button'
            };

            // تنظيف القائمة ما عدا زر "الكل"
            const allBtn = document.querySelector('.brand-filter[data-brand="all"]');
            brandsContainer.innerHTML = '';
            brandsContainer.appendChild(allBtn);

            // إضافة زر "الكل" مرة أخرى للأمان
            allBtn.addEventListener('click', () => {
                document.querySelectorAll('.brand-filter').forEach(b => b.classList.remove('active'));
                allBtn.classList.add('active');
                displayPhones(allPhonesData);
            });

            // إنشاء أزرار الشركات
            brands.forEach(brand => {
                const btn = document.createElement('button');
                btn.className = 'brand-filter';
                btn.dataset.brand = brand.brand_name;
                
                // تحديد الأيقونة المناسبة
                const iconClass = brandIcons[brand.brand_name] || brandIcons['default'];

                btn.innerHTML = `<i class="${iconClass}"></i> <span>${brand.brand_name}</span>`;
                
                btn.addEventListener('click', () => {
                    document.querySelectorAll('.brand-filter').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    filterPhonesByBrand(brand.brand_name);
                });

                brandsContainer.appendChild(btn);
            });

        } catch (err) {
            console.error("Error loading brands:", err);
        }
    }

    function filterPhonesByBrand(brandName) {
        const filtered = allPhonesData.filter(p => 
            p.brand_name.toLowerCase() === brandName.toLowerCase()
        );
        displayPhones(filtered);
    }

    // --- 2. تحميل وعرض الهواتف ---
    async function loadPhones() {
        try {
            const res = await fetch(`${API_URL}/api/phones`);
            if (!res.ok) throw new Error('Server Error');
            allPhonesData = await res.json();
            displayPhones(allPhonesData);
        } catch (err) {
            phoneGrid.innerHTML = `<p style="color:#ef4444; text-align:center; grid-column: 1/-1;">خطأ في الاتصال بالسيرفر: ${err.message}</p>`;
        }
    }

    function displayPhones(phones) {
        phoneGrid.innerHTML = '';
        if (phones.length === 0) {
            phoneGrid.innerHTML = '<p style="text-align:center; grid-column: 1/-1; color: var(--text-muted)">لا توجد نتائج مطابقة.</p>';
            return;
        }

        phones.forEach(phone => {
            const price = phone.price > 0 ? `${phone.price.toLocaleString()}` : 'غير متوفر';
            const img = phone.image_url || 'https://via.placeholder.com/200?text=No+Image';
            
            const ramDisplay = phone.ram ? phone.ram.replace(/\D/g, '') + ' GB' : 'N/A';

            // HTML الكارت الجديد
            const card = `
                <div class="phone-card" data-id="${phone.phone_id}">
                    <img src="${img}" class="phone-card-image" loading="lazy" alt="${phone.full_name}">
                    <div class="card-header">
                        <span>${phone.full_name}</span>
                    </div>
                    
                    <div class="card-specs">
                        <span class="spec-item"><i class="fa-solid fa-memory"></i> ${ramDisplay}</span>
                        <span class="spec-item"><i class="fa-solid fa-battery-full"></i> ${phone.battery}</span>
                        <span class="spec-item"><i class="fa-solid fa-camera"></i> ${phone.camera}</span>
                    </div>

                    <div class="card-footer">
                        <span class="phone-price">${price} ج.م</span>
                        <label>
                            <input type="checkbox" class="compare-cb" data-name="${phone.full_name}">
                            قارن
                        </label>
                    </div>
                </div>
            `;
            phoneGrid.innerHTML += card;
        });

        // إعادة ربط الـ Checkboxes بالحالة الحالية
        document.querySelectorAll('.compare-cb').forEach(cb => {
            cb.checked = comparisonList.includes(cb.dataset.name);
            cb.addEventListener('change', handleCheck);
        });
    }

    function setupEvents() {
        // البحث
        searchInput.addEventListener('input', (e) => { // تغيير إلى input للبحث الفوري
            const val = searchInput.value.trim().toLowerCase();
            const filtered = allPhonesData.filter(p => p.full_name.toLowerCase().includes(val));
            displayPhones(filtered);
        });

        // تفريغ المقارنة
        clearComparisonBtn.addEventListener('click', () => {
            comparisonList = [];
            updateCompareUI();
            displayPhones(allPhonesData); 
        });

        // إغلاق النافذة المنبثقة
        modalCloseBtn.addEventListener('click', () => modalOverlay.style.display = 'none');
        modalOverlay.addEventListener('click', (e) => { if(e.target === modalOverlay) modalOverlay.style.display='none'; });

        // --- أحداث الشات بوت (الجديد) ---
        chatbotToggler.addEventListener('click', () => document.body.classList.toggle('show-chatbot'));
        closeChatBtn.addEventListener('click', () => document.body.classList.remove('show-chatbot'));
        
        chatSend.addEventListener('click', sendChatMessage);
        chatInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendChatMessage();
            }
        });
    }

    // --- 3. منطق المقارنة ---
    function handleCheck(e) {
        const name = e.target.dataset.name;
        if (e.target.checked) {
            if (comparisonList.length < 2) {
                comparisonList.push(name);
            } else {
                e.target.checked = false;
                alert("يمكنك مقارنة جهازين فقط في نفس الوقت.");
            }
        } else {
            comparisonList = comparisonList.filter(n => n !== name);
        }
        updateCompareUI();

        if (comparisonList.length === 2) {
            fetchComparison(comparisonList[0], comparisonList[1]);
        }
    }

    function updateCompareUI() {
        const count = comparisonList.length;
        clearComparisonBtn.innerHTML = `<i class="fa-solid fa-trash-can"></i> تفريغ المقارنة (${count})`;
    }

    async function fetchComparison(name1, name2) {
        modalOverlay.style.display = 'flex';
        modalLoader.style.display = 'block';
        comparisonTableBody.innerHTML = '';
        comparisonTableHeader.innerHTML = '';
        
        try {
            const url = `${API_URL}/api/compare-by-name?phone1_name=${encodeURIComponent(name1)}&phone2_name=${encodeURIComponent(name2)}`;
            const res = await fetch(url);
            const data = await res.json();
            
            if (!res.ok) throw new Error(data.error || 'Error');

            renderComparisonTable(data.phone1, data.phone2, data.all_specs);
            modalLoader.style.display = 'none';
        } catch (err) {
            modalLoader.style.display = 'none';
            comparisonTableBody.innerHTML = `<tr><td colspan="3" style="color:red; text-align:center">${err.message}</td></tr>`;
        }
    }

    function renderComparisonTable(p1, p2, specs) {
        comparisonTableHeader.innerHTML = `
            <th>المواصفات</th>
            <th style="color:var(--accent)">${p1.brand_name} ${p1.model_name}</th>
            <th style="color:var(--accent)">${p2.brand_name} ${p2.model_name}</th>
        `;
        
        let html = `
            <tr>
                <td>الصورة</td>
                <td><img src="${p1.image_url}" class="comparison-image"></td>
                <td><img src="${p2.image_url}" class="comparison-image"></td>
            </tr>
            <tr>
                <td>السعر</td>
                <td class="${p1.price < p2.price && p1.price > 0 ? 'spec-winner' : 'spec-loser'}">${p1.price} ج.م</td>
                <td class="${p2.price < p1.price && p2.price > 0 ? 'spec-winner' : 'spec-loser'}">${p2.price} ج.م</td>
            </tr>
        `;

        const importantSpecs = ['RAM', 'Capacity', 'Screen Size', 'Main Camera', 'Chipset', 'Internal'];
        
        // دالة مساعدة لتنظيف الأرقام للمقارنة
        const parseNum = (str) => {
            if(!str) return 0;
            const match = str.match(/(\d+(\.\d+)?)/);
            return match ? parseFloat(match[0]) : 0;
        };

        importantSpecs.forEach(k => {
            const v1 = p1.specs[k] || '-';
            const v2 = p2.specs[k] || '-';
            
            let c1 = '', c2 = '';
            
            // منطق بسيط لتلوين الفائز
            const n1 = parseNum(v1);
            const n2 = parseNum(v2);

            if (n1 > 0 && n2 > 0) {
                if (n1 > n2) { c1 = 'spec-winner'; c2 = 'spec-loser'; }
                else if (n2 > n1) { c1 = 'spec-loser'; c2 = 'spec-winner'; }
            }

            html += `<tr><td>${k}</td><td class="${c1}">${v1}</td><td class="${c2}">${v2}</td></tr>`;
        });

        comparisonTableBody.innerHTML = html;
    }

    // --- 4. منطق الشات بوت ---
    async function sendChatMessage() {
        const text = chatInput.value.trim();
        if (!text) return;

        addMsg('user', text);
        chatInput.value = '';
        
        // رسالة انتظار
        const loadingId = addMsg('bot', 'جاري الكتابة...');

        try {
            const res = await fetch(`${API_URL}/api/chat`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ message: text })
            });
            const data = await res.json();
            
            // حذف رسالة الانتظار
            const loadMsg = document.getElementById(loadingId);
            if (loadMsg) loadMsg.remove();
            
            if (data.error) addMsg('bot', 'عذراً، حدث خطأ: ' + data.error);
            else addMsg('bot', data.reply);

        } catch (err) {
            const loadMsg = document.getElementById(loadingId);
            if (loadMsg) loadMsg.remove();
            addMsg('bot', 'خطأ في الاتصال بالسيرفر.');
        }
    }

    function addMsg(role, text) {
        const li = document.createElement('li');
        li.className = `chat-message ${role}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        // إضافة أيقونة للبوت فقط
        if(role === 'bot') {
            contentDiv.innerHTML = `<i class="fa-solid fa-robot bot-icon-small" style="display:inline-block; margin-left:5px"></i> ${text}`;
        } else {
            contentDiv.textContent = text;
        }

        li.appendChild(contentDiv);
        
        const id = 'msg-' + Date.now();
        li.id = id;
        
        chatMessages.appendChild(li);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return id;
    }
});