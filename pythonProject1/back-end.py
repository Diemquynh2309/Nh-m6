from flask import Flask, request, jsonify, render_template, redirect, url_for
import mysql.connector
from mysql.connector import cursor

app = Flask(__name__)
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'novano123'
DB_NAME = 'namnhac'


# Kết nối tới cơ sở dữ liệu
def create_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


@app.route("/", methods=["GET"])
def register_page():
    return render_template('dangnhap.html')


# Tuyến đường xử lý yêu cầu đăng ký
@app.route("/", methods=["POST"])
def login():
    try:
        # Kết nối tới cơ sở dữ liệu
        conn = create_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Lấy dữ liệu từ form HTML
        username = request.form.get("username")
        password = request.form.get("password")

        # Thực hiện truy vấn SELECT
        cursor.execute("SELECT * FROM ThongTinDangNhap WHERE TaiKhoan = %s", (username,))
        result = cursor.fetchone()

        # Đóng kết nối và tài nguyên
        cursor.close()
        conn.close()

        if result and result["MatKhau"] == password:
            return redirect(url_for("trangchu"))
        else:
            return jsonify({"message": "Thong tin sai roi dit me may"})


    except Exception as error:

        return jsonify({"error": "Đã xảy ra lỗi: " + str(error)}), 500

@app.route("/trangchu", methods=["GET"])
def trangchu():
    # Xử lý logic khi người dùng truy cập trang "/themhang" bằng phương thức GET
    return render_template('trangchu.html')


@app.route("/kho", methods=["POST"])
def kho():
    # Xử lý logic khi người dùng truy cập trang "/themhang" bằng phương thức GET
    return render_template('index.html')

@app.route("/kho", methods=["GET"])
def get_data():
    try:
        search = request.args.get("search")
        # Kết nối tới cơ sở dữ liệu
        conn = create_db_connection()
        cursor = conn.cursor(dictionary=True)

        if search is not None:
            query = "SELECT * FROM KhoHang WHERE TenHang like %s"
            # cursor.execute("SELECT * FROM KhoHang")
            search_value = "%" + search + "%"
            cursor.execute(query, (search_value,))
            results = cursor.fetchall()
            results = list(results)
        else:
            # Thực hiện truy vấn SELECT
            cursor.execute("SELECT * FROM KhoHang")
            results = cursor.fetchall()

        # Đóng kết nối và tài nguyên
        cursor.close()
        conn.close()

        data = {"results": results}
        print (search)
        # print(data)
        # Trả về kết quả dạng HTML
        return render_template('index.html', data=data)
    except mysql.connector.Error as error:
        print("Lỗi khi truy vấn dữ liệu từ cơ sở dữ liệu: {}".format(error))
        return jsonify({"error": "Đã xảy ra lỗi"}), 500



@app.route("/themhang", methods=["GET"])
def them_hang():
    # Xử lý logic khi người dùng truy cập trang "/themhang" bằng phương thức GET
    return render_template('themhang.html')


# @app.route("/themhang", methods=["POST"])
# def themhang():
#     try:
#         # Nhận thông tin từ request
#         ten_hang = request.form.get("ten_hang")
#         so_luong = request.form.get("so_luong")
#         don_vi_tinh = request.form.get("don_vi_tinh")
#         don_gia = request.form.get("don_gia")
#         don_gia_ban = request.form.get("don_gia_ban")
#
#         # Kết nối tới cơ sở dữ liệu
#         conn = create_db_connection()
#         cursor = conn.cursor()
#
#         # Thực hiện truy vấn INSERT
#         insert_query = "INSERT INTO KhoHang (TenHang, SoLuong, DonViTinh, DonGia, DonGiaBan) VALUES (%s, %s, %s, %s, %s)"
#         cursor.execute(insert_query, (ten_hang, so_luong, don_vi_tinh, don_gia, don_gia_ban))
#
#         # Commit các thay đổi và đóng kết nối
#         conn.commit()
#         cursor.close()
#         conn.close()
#
#         # Trả về kết quả
#         return redirect(url_for("get_data"))
#     except:
#         return jsonify({"error": "Đã xảy ra lỗi"}), 500



@app.route("/themhang", methods=["POST"])
def xu_ly_them_hang():
    if request.method == "POST":
        try:
            # Lấy thông tin từ dữ liệu POST
            ten_hang = request.form.get("ten_hang")
            so_luong = request.form.get("so_luong")
            don_vi_tinh = request.form.get("don_vi_tinh")
            don_gia = request.form.get("don_gia")
            gia_ban = request.form.get("gia_ban")

            # Kết nối tới cơ sở dữ liệu
            conn = create_db_connection()
            cursor = conn.cursor()

            # Thực hiện truy vấn INSERT
            insert_query = "INSERT INTO KhoHang (TenHang, SoLuong, DonViTinh, DonGia, DonGiaBan) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (ten_hang, so_luong, don_vi_tinh, don_gia, gia_ban))

            # Commit các thay đổi và đóng kết nối
            conn.commit()
            cursor.close()
            conn.close()

            # Chuyển hướng trở lại trang chính
            return redirect(url_for("get_data"))
        except mysql.connector.Error as error:
            print("Lỗi khi thêm dữ liệu vào cơ sở dữ liệu: {}".format(error))
            return jsonify({"error": "Dit me loi~ roi"}), 500

# @app.route("/sua", methods=["GET"])
# def xoa_hang():
#     # Xử lý logic khi người dùng truy cập trang "/themhang" bằng phương thức GET
#     return render_template('delete.html')

@app.route("/sua", methods=["POST"])
def sua():
    try:
        # Nhận thông tin từ request
        ten_hang = request.form.get("tenhang_sua")
        so_luong = request.form.get("soluong_sua")
        don_vi_tinh = request.form.get("donvitinh_sua")
        don_gia = request.form.get("dongia_sua")
        gia_ban = request.form.get("giaban_sua")
        submit_value = request.form.get("submit_button")
        print(ten_hang, so_luong, don_vi_tinh, don_gia, gia_ban)
        # Thực hiện sua hàng trong cơ sở dữ liệu
        conn = create_db_connection()
        cursor = conn.cursor()

        if submit_value == "Sửa":
            query = "UPDATE KhoHang SET SoLuong = %s, DonViTinh = %s, DonGia = %s, DonGiaBan = %s WHERE TenHang = %s"
            cursor.execute(query, (so_luong, don_vi_tinh, don_gia, gia_ban, ten_hang))
        if submit_value == "Xoá":
            print(submit_value)
            query = "DELETE FROM KhoHang WHERE TenHang = %(name)s"
            cursor.execute(query, {'name':ten_hang})

        conn.commit()
        cursor.close()
        conn.close()

        # Trả về kết quả
        return redirect(url_for("get_data"))
    except:
        return jsonify({"error": "loi roi"}), 500


@app.route("/danhsachhoadon", methods=["POST"])
def ds_hoadon():
    # Xử lý logic khi người dùng truy cập trang "/themhang" bằng phương thức GET
    return render_template('danhsachhoadon.html')

@app.route("/danhsachhoadon", methods=["GET"])
def hoa_don():
    try:
        search = request.args.get("search")
        # Kết nối tới cơ sở dữ liệu
        conn = create_db_connection()
        cursor = conn.cursor(dictionary=True)

        if search is not None:
            query = "SELECT * FROM KhoHang WHERE HoaDon like %s"
            # cursor.execute("SELECT * FROM KhoHang")
            search_value = "%" + search + "%"
            cursor.execute(query, (search_value,))
            results = cursor.fetchall()
            results = list(results)
        else:
            # Thực hiện truy vấn SELECT
            cursor.execute("SELECT * FROM HoaDon")
            results = cursor.fetchall()

        # Đóng kết nối và tài nguyên
        cursor.close()
        conn.close()

        data = {"results": results}
        print (data)
        # print(data)
        # Trả về kết quả dạng HTML
        return render_template('danhsachhoadon.html', data=data)
    except mysql.connector.Error as error:
        print("Lỗi khi truy vấn dữ liệu từ cơ sở dữ liệu: {}".format(error))
        return jsonify({"error": "Đã xảy ra lỗi"}), 500

@app.route("/taodonhang", methods=["POST"])
def don():
    # Xử lý logic khi người dùng truy cập trang "/themhang" bằng phương thức GET
    return render_template('demotaodonhang.html')


# Một danh sách các sản phẩm trong kho (được giả định là dữ liệu từ cơ sở dữ liệu)


@app.route('/taohonhang', methods=['GET'])
def taohonhang():
    search_value = request.args.get('search')

    # Thực hiện quá trình tìm kiếm sản phẩm dựa trên search_value
    # Ví dụ: Sử dụng cơ sở dữ liệu hoặc các phương thức khác để tìm kiếm sản phẩm

    # Giả sử kết quả tìm kiếm được trả về dưới dạng danh sách các đối tượng sản phẩm
    search_results = [
        {
            'TenHang': 'Sản phẩm 1',
            'DonGiaBan': 100
        },
        {
            'TenHang': 'Sản phẩm 2',
            'DonGiaBan': 200
        },
        {
            'TenHang': 'Sản phẩm 3',
            'DonGiaBan': 300
        }
    ]

    data = {'results': search_results}
    return render_template('index.html', data=data)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')




# @app.route('/taodonhang', methods=["GET"])
# def taodonhang():
#     try:
#         tong_tien = 0
#         search = request.args.get("search")
#         sanpham = request.form.get("tensanpham")
#         # Kết nối tới cơ sở dữ liệu
#         conn = create_db_connection()
#         cursor = conn.cursor(dictionary=True)
#
#         if search is not None:
#             query = "SELECT * FROM KhoHang WHERE TenHang LIKE %s"
#             search_value = "%" + search + "%"
#             cursor.execute(query, (search_value,))
#             results = cursor.fetchall()
#             results = list(results)
#         # else:
#         #     # Thực hiện truy vấn SELECT để lấy danh sách sản phẩm từ cơ sở dữ liệu
#         #     cursor.execute("SELECT * FROM KhoHang")
#         #     results = cursor.fetchall()
#
#         if request.method == "POST":
#             list_san_pham = request.form.getlist("san_pham")
#             so_luong_list = request.form.getlist("so_luong")
#
#             for i in range(len(list_san_pham)):
#                 san_pham_id = list_san_pham[i]
#                 so_luong = int(so_luong_list[i])
#
#                 # Thực hiện truy vấn SELECT để lấy thông tin sản phẩm từ cơ sở dữ liệu
#                 cursor.execute("SELECT * FROM KhoHang WHERE ID = %s", (san_pham_id,))
#                 san_pham = cursor.fetchone()
#
#                 thanh_tien = san_pham['DonGia'] * so_luong
#                 tong_tien += thanh_tien
#
#         cursor.close()
#         conn.close()
#         print(search)
#         print(sanpham)
#
#         data = {"list_san_pham": results, "tong_tien": tong_tien, "search": search}
#         return render_template('demotaodonhang.html', data=data)
#
#     except mysql.connector.Error as error:
#         print("Lỗi khi truy vấn dữ liệu từ cơ sở dữ liệu: {}".format(error))
#         return jsonify({"error": "Đã xảy ra lỗi"}), 500

@app.route("/taohoadon", methods=["GET"])
def taohoadon_():
    # Xử lý logic khi người dùng truy cập trang "/themhang" bằng phương thức GET
    return render_template('taohoadon.html')

@app.route("/taohoadon", methods=["POST"])
def create_invoice():
    try:
        # Nhận dữ liệu từ form HTML
        ten_khach_hang = request.form.get("ten_khach_hang")
        so_dien_thoai = request.form.get("so_dien_thoai")
        tong_thanh_tien = request.form.get("tong_thanh_tien")
        trang_thai = request.form.get("trang_thai")

        # Kết nối tới cơ sở dữ liệu
        conn = create_db_connection()
        cursor = conn.cursor()

        # Thêm hoá đơn vào bảng HoaDon
        query = "INSERT INTO HoaDon (TenKhachHang, SoTienThanhToan, TrangThai) VALUES (%s, %s, %s)"
        values = (ten_khach_hang, tong_thanh_tien, trang_thai)
        cursor.execute(query, values)

        # Kiểm tra trạng thái hoá đơn
        if trang_thai != "DaThanhToan":
            # Kiểm tra sự tồn tại của tên khách hàng trong bảng ThongTinKhachHang
            query_check = "SELECT TenKhachHang FROM ThongTinKhachHang WHERE TenKhachHang = %s"
            cursor.execute(query_check, (ten_khach_hang,))
            existing_customer = cursor.fetchone()

            if existing_customer:
                # Tên khách hàng đã tồn tại, cộng thêm nợ
                query_update = "UPDATE ThongTinKhachHang SET TongTienNo = TongTienNo + %s WHERE TenKhachHang = %s"
                values_update = (tong_thanh_tien, ten_khach_hang)
                cursor.execute(query_update, values_update)
            else:
                # Tên khách hàng chưa tồn tại, thêm bản ghi mới
                query_insert = "INSERT INTO ThongTinKhachHang (TenKhachHang, SDT, TongTienNo, TrangThai) VALUES (%s, %s, %s, %s)"
                values_insert = (ten_khach_hang, so_dien_thoai, tong_thanh_tien, "Chua Thanh Toan")
                cursor.execute(query_insert, values_insert)

        # Lưu thay đổi và đóng kết nối
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("get_data"))
    except mysql.connector.Error as error:
        print("Lỗi khi tạo hoá đơn: {}".format(error))
        return jsonify({"error": "Loi~ roi thang loz"}), 500

@app.route("/khachhangno", methods=["POST"])
def khachhangno_():
    # Xử lý logic khi người dùng truy cập trang "/themhang" bằng phương thức GET
    return render_template('khachhangno.html')

@app.route('/khachhangno', methods=["GET"])
def khachhangno():
    try:
        # Kết nối tới cơ sở dữ liệu
        conn = create_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Thực hiện truy vấn SELECT danh sách khách hàng
        cursor.execute("SELECT * FROM ThongTinKhachHang")
        list_khach_hang = cursor.fetchall()

        cursor.close()
        conn.close()

        data = {"list_khach_hang": list_khach_hang}
        return render_template('khachhangno.html', data=data)

    except mysql.connector.Error as error:
        print("Lỗi khi truy vấn dữ liệu từ cơ sở dữ liệu: {}".format(error))
        return jsonify({"error": "Đã xảy ra lỗi"}), 500


if __name__ == "__main__":
    app.run()