/*加到function.php */
function render_custom_form() {
    ob_start(); ?>
	 <form id="custom-form">
			<h3>客戶資訊</h3>
			<div class="form-group">
				<div class="form-row">
					<label>業主名稱：</label>
					<input type="text" name="name" value="">
				</div>
				<div class="form-row">
					<label>聯絡電話：</label>
					<input type="text" name="phone" value="">
				</div>
			</div>
			<div class="form-group">
				<div class="form-row">
					<label>日期：</label>
					<input type="text" name="date" value="">
				</div>
				<div class="form-row">
					<label>訂製期：</label>
					<input type="text" name="lead_time" value="">
				</div>
			</div>
			<div class="form-group">
				<div class="form-row">
					<label>施作地點：</label>
					<input type="text" name="location" value="">
				</div>
				<div class="form-row">
					<label>行銷業務：</label>
					<input type="text" name="sales" value="">
				</div>
			</div>

			<h3>折扣與贈送</h3>
			<div class="form-group">
				<div class="form-row">
					<label>折扣 (%)：</label>
					<input type="text" name="discount" value="0">
				</div>
				<div class="form-row">
					<label>贈送金額：</label>
					<input type="text" name="gift" value="0">
				</div>
			</div>

			<h3>商品明細</h3>
			<div style="overflow-x: auto;">
				<table id="items-table">
					<thead>
						<tr>
							<th>NO</th>
							<th>品項</th>
							<th>數量</th>
							<th>價格/元</th>
							<th>備註</th>
							<th>操作</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td data-label="NO"><input type="text" name="items[0][no]" value=""></td>
							<td data-label="品項"><input type="text" name="items[0][item]" value=""></td>
							<td data-label="數量"><input type="text" name="items[0][quantity]" value=""></td>
							<td data-label="價格/元"><input type="text" name="items[0][price]" value=""></td>
							<td data-label="備註"><input type="text" name="items[0][remark]" value=""></td>
							<td data-label="操作"><button type="button" class="delete-row">刪除</button></td>
						</tr>
					</tbody>
				</table>
			</div>

			<button type="button" id="add-row">新增一行</button>
			<button type="button" id="submit-form">提交</button>
	</form>
    <?php
    return ob_get_clean();
}
add_shortcode('custom_form', 'render_custom_form');
