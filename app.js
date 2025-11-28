document.addEventListener('DOMContentLoaded', () => {
    const API_URL = 'http://127.0.0.1:5000';

    // Elements
    const phoneGrid = document.getElementById('phone-grid');
    const searchInput = document.getElementById('search-input');
    const brandFilters = document.querySelectorAll('.brand-filter');
    const clearComparisonBtn = document.querySelector('.clear-comparison');
    
    // Modal Elements
    const modalOverlay = document.getElementById('comparison-modal-overlay');
    const modalCloseBtn = document.getElementById('modal-close-btn');
    const modalLoader = document.getElementById('modal-loader');
    const comparisonTableBody = document.getElementById('comparison-table-body');
    const comparisonTableHeader = document.getElementById('comparison-table-header');

    // Chat Elements
    const chatInput = document.getElementById("chat-input");
    const chatSend = document.getElementById("chat-send");
    const chatMessages = document.getElementById("chat-messages");
    const chatContainer = document.querySelector('.chatbot-container');
    const toggleChatBtn = document.getElementById('toggle-chat');

    let allPhonesData = [];
    let comparisonList = [];

    // --- Initialization ---
    init();

    async function init() {
        await loadPhones();
        setupEvents();
        // داخل دالة setupEvents ...
    
    // Admin Button Logic
    const adminBtn = document.getElementById('admin-launcher');
    if (adminBtn) {
        adminBtn.addEventListener('click', () => {
            alert(
                "تنبيه للمدير:\n" +
                "لإدارة الهواتف (إضافة/حذف)، يرجى تشغيل برنامج:\n" +
                "admin_dashboard.py\n" +
                "الموجود في مجلد المشروع على السيرفر."
            );
        });
    }
    }

    // --- Core Functions ---
    async function loadPhones() {
        try {
            const res = await fetch(`${API_URL}/api/phones`);
            if (!res.ok) throw new Error('Server Error');
            allPhonesData = await res.json();
            displayPhones(allPhonesData);
        } catch (err) {
            phoneGrid.innerHTML = `<p style="color:red; text-align:center">خطأ في الاتصال بالسيرفر: ${err.message}</p>`;
        }
    }

    function displayPhones(phones) {
        phoneGrid.innerHTML = '';
        if (phones.length === 0) {
            phoneGrid.innerHTML = '<p style="text-align:center; grid-column: 1/-1;">لا توجد نتائج.</p>';
            return;
        }

        phones.forEach(phone => {
            const price = phone.price > 0 ? `${phone.price.toLocaleString()} ج.م` : 'غير متوفر';
            const img = phone.image_url || 'https://via.placeholder.com/200?text=No+Image';
            
            // استخراج أول رقم من الرام للعرض
            const ramDisplay = phone.ram.replace(/\D/g, '') + ' GB';

            const card = `
                <div class="phone-card" data-id="${phone.phone_id}">
                    <img src="${img}" class="phone-card-image" loading="lazy">
                    <div class="card-header">
                        <span>${phone.full_name}</span>
                        <span class="phone-price">${price}</span>
                    </div>
                    <div class="card-specs">
                        <span class="spec-item">RAM: ${ramDisplay}</span>
                        <span class="spec-item">Bat: ${phone.battery}</span>
                    </div>
                    <div class="card-footer">
                        <label style="cursor:pointer; display:flex; align-items:center; gap:5px">
                            <input type="checkbox" class="compare-cb" data-name="${phone.full_name}">
                            قارن
                        </label>
                    </div>
                </div>
            `;
            phoneGrid.innerHTML += card;
        });

        document.querySelectorAll('.compare-cb').forEach(cb => {
            cb.checked = comparisonList.includes(cb.dataset.name);
            cb.addEventListener('change', handleCheck);
        });
    }

    function setupEvents() {
        // Search
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const val = searchInput.value.trim();
                if (val.toLowerCase().includes('vs')) {
                    const [p1, p2] = val.split(/vs/i);
                    if (p1 && p2) fetchComparison(p1.trim(), p2.trim());
                } else {
                    const filtered = allPhonesData.filter(p => p.full_name.toLowerCase().includes(val.toLowerCase()));
                    displayPhones(filtered);
                }
            }
        });

        // Filter
        brandFilters.forEach(btn => {
            btn.addEventListener('click', () => {
                brandFilters.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                const brand = btn.dataset.brand;
                if (brand === 'all') displayPhones(allPhonesData);
                else displayPhones(allPhonesData.filter(p => p.full_name.includes(brand)));
            });
        });

        // Clear Comparison
        clearComparisonBtn.addEventListener('click', () => {
            comparisonList = [];
            updateCompareUI();
            displayPhones(allPhonesData); // refresh checkboxes
        });

        // Modal
        modalCloseBtn.addEventListener('click', () => modalOverlay.style.display = 'none');
        modalOverlay.addEventListener('click', (e) => { if(e.target===modalOverlay) modalOverlay.style.display='none'; });

        // Chatbot Events
        chatSend.addEventListener('click', sendChatMessage);
        chatInput.addEventListener('keypress', (e) => { if(e.key==='Enter') sendChatMessage(); });
        
        toggleChatBtn.addEventListener('click', () => {
            const isMinimized = chatContainer.style.height === '50px';
            chatContainer.style.height = isMinimized ? 'auto' : '50px';
            toggleChatBtn.textContent = isMinimized ? '−' : '+';
        });
    }

    // --- Comparison Logic ---
    function handleCheck(e) {
        const name = e.target.dataset.name;
        if (e.target.checked) {
            if (comparisonList.length < 2) {
                comparisonList.push(name);
            } else {
                e.target.checked = false;
                alert("يمكنك مقارنة جهازين فقط.");
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
        clearComparisonBtn.innerText = `مسح المقارنة (${comparisonList.length})`;
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
            comparisonTableBody.innerHTML = `<tr><td colspan="3" style="color:red">${err.message}</td></tr>`;
        }
    }

    function renderComparisonTable(p1, p2, specs) {
        comparisonTableHeader.innerHTML = `<th>المواصفات</th><th>${p1.name}</th><th>${p2.name}</th>`;
        
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

        const importantSpecs = ['RAM', 'Capacity', 'Screen Size', 'Main Camera', 'Chipset'];
        importantSpecs.forEach(k => {
            const v1 = p1.specs[k] || '-';
            const v2 = p2.specs[k] || '-';
            // Simple logic to highlight numbers
            const n1 = parseFloat(v1);
            const n2 = parseFloat(v2);
            let c1 = '', c2 = '';
            
            if (!isNaN(n1) && !isNaN(n2)) {
                if (n1 > n2) { c1 = 'spec-winner'; c2 = 'spec-loser'; }
                else if (n2 > n1) { c1 = 'spec-loser'; c2 = 'spec-winner'; }
            }

            html += `<tr><td>${k}</td><td class="${c1}">${v1}</td><td class="${c2}">${v2}</td></tr>`;
        });

        comparisonTableBody.innerHTML = html;
    }

    // --- Chatbot Logic (Connected to Gemini) ---
    async function sendChatMessage() {
        const text = chatInput.value.trim();
        if (!text) return;

        addMsg('user', text);
        chatInput.value = '';

        // إضافة مؤشر الكتابة
        const loadingId = addMsg('bot', 'جاري الكتابة...');

        try {
            const res = await fetch(`${API_URL}/api/chat`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ message: text })
            });
            const data = await res.json();
            
            // إزالة مؤشر الكتابة وتحديث الرسالة
            const loadMsg = document.getElementById(loadingId);
            if (loadMsg) loadMsg.remove();
            
            if (data.error) addMsg('bot', 'حدث خطأ: ' + data.error);
            else addMsg('bot', data.reply);

        } catch (err) {
            addMsg('bot', 'خطأ في الاتصال.');
        }
    }

    function addMsg(role, text) {
        const div = document.createElement('div');
        div.className = `chat-message ${role}`;
        // استخدام marked.js إذا أردت تنسيق Markdown، هنا نص عادي
        div.textContent = text;
        // ID مؤقت
        const id = 'msg-' + Date.now();
        div.id = id;
        
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return id;
    }
});

// --- Admin Logic ---

const adminBtn = document.getElementById('admin-btn');
const passModal = document.getElementById('password-modal');
const passInput = document.getElementById('admin-password-input');
const passSubmit = document.getElementById('submit-password');
const adminDash = document.getElementById('admin-dashboard');
const addPhoneForm = document.getElementById('add-phone-form');

// 1. فتح نافذة الباسورد
adminBtn.addEventListener('click', () => {
    passModal.style.display = 'flex';
    passInput.value = '';
    document.getElementById('password-error').style.display = 'none';
});

// 2. التحقق من الباسورد (بسيط)
passSubmit.addEventListener('click', () => {
    const password = passInput.value;
    if (password === "1234") { // الباسورد هنا
        passModal.style.display = 'none';
        adminDash.style.display = 'flex';
        loadBrands(); // تحميل الشركات للقائمة
        loadPhonesForDelete(); // تحميل الموبايلات للحذف
    } else {
        document.getElementById('password-error').style.display = 'block';
    }
});

// 3. التبديل بين التبويبات
window.showTab = function(tabId) {
    document.getElementById('add-phone-tab').style.display = 'none';
    document.getElementById('delete-phone-tab').style.display = 'none';
    document.getElementById(tabId).style.display = 'block';
}

// 4. تحميل الشركات (للقائمة المنسدلة)
async function loadBrands() {
    try {
        const res = await fetch(`${API_URL}/api/brands`);
        const brands = await res.json();
        const select = document.getElementById('new-brand');
        select.innerHTML = '<option value="">اختر الشركة</option>';
        brands.forEach(b => {
            select.innerHTML += `<option value="${b.brand_id}">${b.brand_name}</option>`;
        });
    } catch (e) { console.error(e); }
}

// 5. إرسال نموذج الإضافة
addPhoneForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        model_name: document.getElementById('new-model').value,
        brand_id: document.getElementById('new-brand').value,
        price: document.getElementById('new-price').value,
        image_url: document.getElementById('new-image').value,
        ram: document.getElementById('spec-ram').value,
        battery: document.getElementById('spec-battery').value,
        screen: document.getElementById('spec-screen').value,
        camera: document.getElementById('spec-camera').value
    };

    try {
        const res = await fetch(`${API_URL}/api/admin/add`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        const result = await res.json();
        if (result.success) {
            alert('تمت الإضافة بنجاح!');
            addPhoneForm.reset();
            fetchPhones(); // تحديث الصفحة الرئيسية
        } else {
            alert('خطأ: ' + result.error);
        }
    } catch (err) { alert('حدث خطأ في الاتصال'); }
});

// 6. تحميل القائمة للحذف
async function loadPhonesForDelete() {
    const listDiv = document.getElementById('delete-list');
    listDiv.innerHTML = '';
    // نستخدم allPhonesData المحملة مسبقاً
    // تأكد أن allPhonesData معرفة عالمياً في app.js (في الأعلى)
    // إذا لم تكن معرفة، يمكنك جلبها مرة أخرى هنا
    const res = await fetch(`${API_URL}/api/phones`);
    const phones = await res.json();

    phones.forEach(p => {
        const item = document.createElement('div');
        item.style.cssText = "display:flex; justify-content:space-between; padding:10px; border-bottom:1px solid #ccc; align-items:center";
        item.innerHTML = `
            <span>${p.full_name}</span>
            <button onclick="deletePhone(${p.phone_id})" style="background:red; color:white; border:none; padding:5px 10px; cursor:pointer">حذف</button>
        `;
        listDiv.appendChild(item);
    });
}

// 7. دالة الحذف
window.deletePhone = async function(id) {
    if(!confirm('هل أنت متأكد من الحذف؟')) return;
    
    try {
        const res = await fetch(`${API_URL}/api/admin/delete/${id}`, { method: 'DELETE' });
        const result = await res.json();
        if (result.success) {
            alert('تم الحذف');
            loadPhonesForDelete(); // تحديث القائمة
            fetchPhones(); // تحديث الصفحة الرئيسية
        }
    } catch(e) { alert('خطأ في الحذف'); }
}