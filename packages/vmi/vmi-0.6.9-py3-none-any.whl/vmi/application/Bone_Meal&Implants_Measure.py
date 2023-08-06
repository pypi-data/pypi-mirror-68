import glob
import vtk
import numpy as np

import vmi
import math
import pydicom

from PySide2.QtCore import *
from PySide2.QtWidgets import *
from typing import Union, List, Optional, Dict, Any


def addTextActor(view: vmi.View, s: str, p: np.ndarray, f: vtk.vtkFollower):
    text = vtk.vtkVectorText()
    text.SetText(s)
    text.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetRelativeCoincidentTopologyLineOffsetParameters(0, -66000)
    mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(0, -66000)
    mapper.SetRelativeCoincidentTopologyPointOffsetParameter(-66000)
    mapper.SetInputData(text.GetOutput())

    r = 5 * pt_radius
    view.renderer().RemoveActor(f)
    f.SetMapper(mapper)
    f.SetScale(r, r, r)
    f.SetPosition(p)

    view.renderer().AddActor(f)
    f.SetCamera(view.renderer().GetActiveCamera())


# 数据导入
def read_dicom():
    dcmdir = vmi.askDirectory('DICOM')  # 用户选择文件夹

    if dcmdir is not None:  # 判断用户选中了有效文件夹并点击了确认
        series_list = vmi.sortSeries(dcmdir)  # 将文件夹及其子目录包含的所有DICOM文件分类到各个系列
        if len(series_list) > 0:  # 判断该文件夹内包含有效的DICOM系列
            series = vmi.askSeries(series_list)  # 用户选择DICOM系列
            if series is not None:  # 判断用户选中了有效系列并点击了确认

                return series.read()  # 读取DICOM系列为图像数据


def input_pre_ct():
    image_volume[0].setData(read_dicom())
    update_meal_lines()
    image_view[0].setCamera_Coronal()
    image_view[0].setCamera_FitAll()


def input_pst_ct():
    image_volume[1].setData(read_dicom())
    update_meal_lines()
    image_view[1].setCamera_Coronal()
    image_view[1].setCamera_FitAll()


def read_stl():
    file = vmi.askOpenFile('*.stl')

    if file:
        r = vtk.vtkSTLReader()
        r.SetFileName(file)
        r.Update()

        return r.GetOutput()


def read_stp():
    file = vmi.askOpenFile('*.stp', '导入 (Import) STEP')
    sh = vmi.ccOpenFile_STEP(file)
    return sh


def input_pre_meal():
    meal_prop[0].setData(read_stl())
    update_meal_lines()
    co_volume_diff()

    image_view[0].setCamera_Coronal()
    image_view[0].setCamera_FitAll()


def input_pst_meal():
    meal_prop[1].setData(read_stl())
    update_meal_lines()
    co_volume_diff()

    image_view[1].setCamera_Coronal()
    image_view[1].setCamera_FitAll()


def input_pre_imp():
    stp_pd = vmi.ccPd_Sh(read_stp())
    if image_volume[0]:
        vec = vmi.imOrigin(image_volume[0].data()) - stp_pd.GetCenter()
        t = vtk.vtkTransform()
        t.Identity()
        t.PreMultiply()
        t.Translate(vec)
        t.Update()
        stp_pd = vmi.pdTransform(stp_pd, t)

    imp_prop[0].setData(stp_pd)
    image_view[0].setCamera_Coronal()
    image_view[0].setCamera_FitAll()


def input_pst_imp():
    imp_prop[1].setData(read_stl())
    image_view[1].setCamera_Coronal()
    image_view[1].setCamera_FitAll()


# 配准点
def draw_mark_pts():
    pd_list = [[], []]
    for i, pt in enumerate(mark_lists[0]):
        pd_list[0].append(vmi.pdSphere(pt_radius, pt))

        text = vtk.vtkFollower()
        text.SetPickable(False)
        addTextActor(image_view[0], str(i + 1), pt, text)
        text_lists[0].append(text)

    mark_pts_prop[0].setData(vmi.pdAppend(pd_list[0]))

    for i, pt in enumerate(mark_lists[1]):
        pd_list[1].append(vmi.pdSphere(pt_radius, pt))

        text = vtk.vtkFollower()
        text.SetPickable(False)
        addTextActor(image_view[1], str(i + 1), pt, text)
        text_lists[1].append(text)

    mark_pts_prop[1].setData(vmi.pdAppend(pd_list[1]))

    if len(mark_lists[0]) < 3:
        mark_boxes[1].setVisible(False)
    if len(mark_lists[1]) < 3:
        mark_boxes[1].setVisible(False)
    if len(mark_lists[0]) != len(mark_lists[1]):
        mark_boxes[1].setVisible(False)

    if len(mark_lists[0]) > 2 and len(mark_lists[1]) > 2:
        if len(mark_lists[0]) == len(mark_lists[1]):
            mark_boxes[1].setVisible(True)


# 计算配准矩阵
def co_align_matrix():
    internal_pts = vtk.vtkPoints()
    external_pts = vtk.vtkPoints()

    for pt in mark_lists[0]:
        internal_pts.InsertNextPoint(pt)

    for pt in mark_lists[1]:
        external_pts.InsertNextPoint(pt)

    landmark = vtk.vtkLandmarkTransform()
    landmark.SetSourceLandmarks(external_pts)
    landmark.SetTargetLandmarks(internal_pts)
    landmark.SetModeToRigidBody()
    landmark.Update()

    return landmark.GetMatrix()


# 重建配准模型
def bu_align_model():
    pd = [vmi.imIsosurface(image_volume[0].data(), bone_value[0]),
          vmi.imIsosurface(image_volume[1].data(), bone_value[1])]

    t = vtk.vtkTransform()
    t.Identity()
    t.PreMultiply()
    t.SetMatrix(co_align_matrix())
    t.Update()

    align_model_prop[0].setData(pd[0])
    align_model_prop[1].setData(vmi.pdTransform(pd[1], t))

    if meal_prop[0].data().GetNumberOfCells() > 0:
        if meal_prop[1].data().GetNumberOfCells() > 0:
            align_meal_prop[0].setData(meal_prop[0])
            align_meal_prop[1].setData(vmi.pdTransform(meal_prop[1].data(), t))

    if imp_prop[0].data().GetNumberOfCells() > 0:
        if imp_prop[1].data().GetNumberOfCells() > 0:
            align_imp_prop[0].setData(imp_prop[0])
            align_imp_prop[1].setData(vmi.pdTransform(imp_prop[1].data(), t))

    align_view.setCamera_Coronal()
    align_view.setCamera_FitAll()

    mark_lists[0].clear()
    mark_lists[1].clear()

    mark_pts_prop[0].setData(None)
    mark_pts_prop[1].setData(None)

    for t in text_lists[0]:
        image_view[0].renderer().RemoveActor(t)
    for t in text_lists[1]:
        image_view[1].renderer().RemoveActor(t)


def bu_model_frame(pd: vtk.vtkPolyData):
    bounds = pd.GetBounds()

    pts = [np.array([bounds[0], bounds[2], bounds[4]]),
           np.array([bounds[1], bounds[2], bounds[4]]),
           np.array([bounds[0], bounds[3], bounds[4]]),
           np.array([bounds[1], bounds[3], bounds[4]]),
           np.array([bounds[0], bounds[2], bounds[5]]),
           np.array([bounds[1], bounds[2], bounds[5]]),
           np.array([bounds[0], bounds[3], bounds[5]]),
           np.array([bounds[1], bounds[3], bounds[5]])]

    frame = vmi.pdAppend([vmi.ccPd_Sh(vmi.ccWire(vmi.ccSegments([pts[0], pts[1]]))),
                          vmi.ccPd_Sh(vmi.ccWire(vmi.ccSegments([pts[0], pts[2]]))),
                          vmi.ccPd_Sh(vmi.ccWire(vmi.ccSegments([pts[3], pts[1]]))),
                          vmi.ccPd_Sh(vmi.ccWire(vmi.ccSegments([pts[3], pts[2]]))),
                          vmi.ccPd_Sh(vmi.ccWire(vmi.ccSegments([pts[4], pts[5]]))),
                          vmi.ccPd_Sh(vmi.ccWire(vmi.ccSegments([pts[4], pts[6]]))),
                          vmi.ccPd_Sh(vmi.ccWire(vmi.ccSegments([pts[7], pts[5]]))),
                          vmi.ccPd_Sh(vmi.ccWire(vmi.ccSegments([pts[7], pts[6]]))),
                          vmi.ccPd_Sh(vmi.ccWire(vmi.ccSegments([pts[0], pts[4]]))),
                          vmi.ccPd_Sh(vmi.ccWire(vmi.ccSegments([pts[1], pts[5]]))),
                          vmi.ccPd_Sh(vmi.ccWire(vmi.ccSegments([pts[2], pts[6]]))),
                          vmi.ccPd_Sh(vmi.ccWire(vmi.ccSegments([pts[3], pts[7]])))])

    return frame


def co_intersect_pts(pd: vtk.vtkPolyData, spc: np.ndarray, step: int):
    obb = vtk.vtkOBBTree()
    obb.SetDataSet(pd)
    obb.BuildLocator()

    bounds = pd.GetBounds()
    height = np.abs(bounds[5] - bounds[4])
    width = np.abs(bounds[1] - bounds[0])

    pt = [np.array([bounds[0], bounds[2], bounds[4]]),
          np.array([bounds[0], bounds[3], bounds[4]])]

    j_spc = spc[2] * step
    i_spc = spc[0] * step

    j_step = int(height / j_spc)
    i_step = int(width / i_spc)

    intersect_pts = []
    for j_num in range(j_step):
        hor_pts = []
        for i_num in range(i_step):
            pt[0][0] += i_spc
            pt[1][0] += i_spc

            intersect_points = vtk.vtkPoints()
            cell_id_list = vtk.vtkIdList()

            intersect = obb.IntersectWithLine(pt[0], pt[1], intersect_points, cell_id_list)
            if intersect:
                first_p = intersect_points.GetPoint(0)
                count = intersect_points.GetNumberOfPoints()
                if count >= 2:
                    end_p = intersect_points.GetPoint(count - 1)

                    hor_pts.append([first_p, end_p])
                else:
                    hor_pts.append([[0, 0, 0], [0, 0, 0]])
            else:
                hor_pts.append([[0, 0, 0], [0, 0, 0]])

        intersect_pts.append(hor_pts)

        pt[0][0] -= i_spc * i_step
        pt[1][0] -= i_spc * i_step
        pt[0][2] += j_spc
        pt[1][2] += j_spc

    return intersect_pts


def bu_intersect_lines(pts_list):
    lines_pd_list = []
    for hor_pts in pts_list:
        for pts in hor_pts:
            if pts[0] != [0, 0, 0]:
                lines_pd_list.append(vmi.pdSphere(0.1, pts[0]))

    return vmi.pdAppend(lines_pd_list)


def co_intersect_data(pts_list, pd: vtk.vtkPolyData):
    if pd.GetNumberOfCells() <= 0:
        return

    rms, mean, max_num, sd = 0, 0, 0, 0
    dis_list, form_list = [], []

    for hor_pts in pts_list:
        hor_form_list = []
        for pts in hor_pts:
            if pts[0] != [0, 0, 0]:
                dis = math.sqrt(math.pow((pts[0][0] - pts[1][0]), 2) + \
                                math.pow((pts[0][1] - pts[1][1]), 2) + \
                                math.pow((pts[0][2] - pts[1][2]), 2))
                dis_list.append(dis)
                hor_form_list.append(dis)
            else:
                hor_form_list.append(0)

        form_list.append(hor_form_list)

    for dis in dis_list:
        rms += math.pow(dis, 2)
        mean += dis

        if dis > max_num:
            max_num = dis

    count = len(dis_list)
    rms = math.sqrt(rms / count)
    mean = mean / count

    for dis in dis_list:
        sd += math.pow(dis - mean, 2)

    sd = math.sqrt(sd / count)

    # 将数据粘贴到剪切板
    copy_list = '\t'
    for num in range(len(pts_list[0])):
        copy_list += 'SP{}'.format(num) + '\t'
    copy_list += '\n'

    for num, hor_list in enumerate(form_list):
        copy_list += 'HP{}'.format(num) + '\t'
        for dis in hor_list:
            copy_list += str(dis) + '\t'
        copy_list += '\n'

    copy_list += '\nlength\twidth\theight\trms\tsd\tmean\tmax\n'
    bounds = pd.GetBounds()
    copy_list += str(bounds[1] - bounds[0]) + '\t'
    copy_list += str(bounds[3] - bounds[2]) + '\t'
    copy_list += str(bounds[5] - bounds[4]) + '\t'
    copy_list += str(rms) + '\t'
    copy_list += str(sd) + '\t'
    copy_list += str(mean) + '\t'
    copy_list += str(max_num) + '\t'

    QApplication.clipboard().setText(copy_list)
    vmi.askInfo('数据已复制到剪贴板！')
    return


def update_meal_lines():
    global meal_pts_list
    data = [meal_prop[0].data(), meal_prop[1].data()]

    if data[0].GetNumberOfCells() > 0:
        if image_volume[0].data().GetNumberOfPoints() > 0:
            meal_pts_list[0] = co_intersect_pts(data[0], vmi.imSpacing(image_volume[0].data()), meal_step[0])
            meal_frame_prop[0].setData(vmi.pdAppend([bu_model_frame(data[0]), bu_intersect_lines(meal_pts_list[0])]))

    if data[1].GetNumberOfCells() > 0:
        if image_volume[1].data().GetNumberOfPoints() > 0:
            meal_pts_list[1] = co_intersect_pts(data[1], vmi.imSpacing(image_volume[1].data()), meal_step[1])
            meal_frame_prop[1].setData(vmi.pdAppend([bu_model_frame(data[1]), bu_intersect_lines(meal_pts_list[1])]))


def co_volume_diff():
    data = [meal_prop[0].data(), meal_prop[1].data()]

    if data[0].GetNumberOfCells() <= 0:
        return
    if data[1].GetNumberOfCells() <= 0:
        return

    mass_properties = [vtk.vtkMassProperties(), vtk.vtkMassProperties()]
    mass_properties[0].SetInputData(data[0])
    mass_properties[0].Update()
    mass_properties[1].SetInputData(data[1])
    mass_properties[1].Update()

    diff = mass_properties[0].GetVolume() - mass_properties[1].GetVolume()

    bone_value_box.draw_text('体积差：{:.2f} mm2'.format(diff))
    bone_value_box.setVisible(True)


def NoButtonWheel(**kwargs):
    global bone_value
    if kwargs['picked'] is bone_value_boxes[0]:
        bone_value[0] = min(max(bone_value[0] + 10 * kwargs['delta'], -1000), 3000)
        bone_value_boxes[0].draw_text('骨阈值：{:.0f} HU'.format(bone_value[0]))
        image_volume[0].setOpacityScalar({bone_value[0] - 1: 0, bone_value[0]: 1})
        return True
    elif kwargs['picked'] is bone_value_boxes[1]:
        bone_value[1] = min(max(bone_value[1] + 10 * kwargs['delta'], -1000), 3000)
        bone_value_boxes[1].draw_text('骨阈值：{:.0f} HU'.format(bone_value[1]))
        image_volume[1].setOpacityScalar({bone_value[1] - 1: 0, bone_value[1]: 1})
        return True
    elif kwargs['picked'] is meal_step_boxes[0]:
        meal_step[0] = min(max(meal_step[0] + kwargs['delta'], 1), 5)
        meal_step_boxes[0].draw_text('间隙：{:.0f} mm'.format(meal_step[0]))
        update_meal_lines()
        return True
    elif kwargs['picked'] is meal_step_boxes[1]:
        meal_step[1] = min(max(meal_step[1] + kwargs['delta'], 1), 5)
        meal_step_boxes[1].draw_text('间隙：{:.0f} mm'.format(meal_step[1]))
        update_meal_lines()
        return True


def LeftButtonPressRelease(**kwargs):
    data = [meal_prop[0].data(), meal_prop[1].data()]
    if kwargs['picked'] is mark_boxes[0]:
        if mark_boxes[0].text() == '开始配准':
            mark_boxes[0].draw_text('选取配准标志点')
            return True
    elif kwargs['picked'] is mark_boxes[1]:
        if len(mark_lists[0]) < 3:
            return
        if len(mark_lists[1]) < 3:
            return
        if len(mark_lists[0]) != len(mark_lists[1]):
            return

        bu_align_model()
        mark_boxes[0].draw_text('开始配准')
        mark_boxes[1].setVisible(False)
        return True
    elif kwargs['picked'] is image_view[0]:
        if kwargs['double'] is True:
            if mark_boxes[0].text() == '选取配准标志点':
                mark_lists[0].append(image_view[0].pickPt_Cell())
                draw_mark_pts()
                return True
    elif kwargs['picked'] is image_view[1]:
        if kwargs['double'] is True:
            if mark_boxes[0].text() == '选取配准标志点':
                mark_lists[1].append(image_view[1].pickPt_Cell())
                draw_mark_pts()
                return True
    elif kwargs['picked'] is meal_data_boxes[0]:
        co_intersect_data(meal_pts_list[0], data[0])
        return True
    elif kwargs['picked'] is meal_data_boxes[1]:
        co_intersect_data(meal_pts_list[1], data[1])
        return True


def return_globals():
    return globals()


if __name__ == '__main__':
    main = vmi.Main(return_globals)
    main.setAppName('Bone_Meal&Implants_Measure')
    main.excludeKeys += ['main']

    menu_input = main.menuBar().addMenu('输入图像')
    menu_input.addAction('选择配准数据').triggered.connect(input_pre_ct)
    menu_input.addAction('选择被配准数据').triggered.connect(input_pst_ct)

    menu_input = main.menuBar().addMenu('骨粉模型')
    menu_input.addAction('选择配准数据').triggered.connect(input_pre_meal)
    menu_input.addAction('选择被配准数据').triggered.connect(input_pst_meal)

    menu_input = main.menuBar().addMenu('种植体')
    menu_input.addAction('选择配准数据').triggered.connect(input_pre_imp)
    menu_input.addAction('选择被配准数据').triggered.connect(input_pst_imp)

    # 原始图像
    image_view = [vmi.View(), vmi.View()]
    for v in image_view:
        v.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]
        v.renderer().SetBackground(0, 0, 0)

    image_volume = [vmi.ImageVolume(image_view[0], pickable=True),
                    vmi.ImageVolume(image_view[1], pickable=True)]

    bone_value = [600, 600]

    for i in range(2):
        image_volume[i].setOpacityScalar({bone_value[i] - 1: 0, bone_value[i]: 1})
        image_volume[i].setColor({bone_value[i]: [1, 1, 0.6]})

    bone_value_boxes = [vmi.TextBox(image_view[0], text='骨阈值：{:.0f} HU'.format(bone_value[0]),
                                    size=[0.2, 0.04], pos=[0, 0.04], anchor=[0, 0], pickable=True),
                        vmi.TextBox(image_view[1], text='骨阈值：{:.0f} HU'.format(bone_value[1]),
                                    size=[0.2, 0.04], pos=[0, 0.04], anchor=[0, 0], pickable=True)]
    for box in bone_value_boxes:
        box.mouse['NoButton']['Wheel'] = [NoButtonWheel]

    # 骨粉模型
    meal_prop = [vmi.PolyActor(image_view[0], color=[1, 1, 1], repres='wireframe', shade=False),
                 vmi.PolyActor(image_view[1], color=[1, 1, 1], repres='wireframe', shade=False)]

    meal_frame_prop = [vmi.PolyActor(image_view[0], color=[1, 0.6, 0.4], line_width=2),
                       vmi.PolyActor(image_view[1], color=[1, 0.6, 0.4], line_width=2)]

    meal_step = [3, 3]
    meal_step_boxes = [vmi.TextBox(image_view[0], text='间隙：{:.0f} mm'.format(meal_step[0]),
                                   size=[0.2, 0.04], pos=[1, 0.04], anchor=[1, 0], pickable=True),
                       vmi.TextBox(image_view[1], text='间隙：{:.0f} mm'.format(meal_step[1]),
                                   size=[0.2, 0.04], pos=[1, 0.04], anchor=[1, 0], pickable=True)]

    meal_data_boxes = [vmi.TextBox(image_view[0], text='导出数据',
                                   size=[0.2, 0.04], pos=[1, 0.08], anchor=[1, 0], pickable=True),
                       vmi.TextBox(image_view[1], text='导出数据',
                                   size=[0.2, 0.04], pos=[1, 0.08], anchor=[1, 0], pickable=True)]
    for box in meal_step_boxes:
        box.mouse['NoButton']['Wheel'] = [NoButtonWheel]
    for box in meal_data_boxes:
        box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

    meal_pts_list = [[], []]

    bone_value_box = vmi.TextBox(image_view[1], text='体积差：{:.2f} mm2'.format(0),
                                 size=[0.2, 0.04], pos=[0, 0.08], anchor=[0, 0], pickable=False)
    bone_value_box.setVisible(False)

    # 种植体
    imp_prop = [vmi.PolyActor(image_view[0], color=[0.4, 0.6, 1], pickable=True),
                vmi.PolyActor(image_view[1], color=[0.4, 0.6, 1])]

    # 配准模块
    mark_pts_prop = [vmi.PolyActor(image_view[0], color=[0.4, 1, 0.6]),
                     vmi.PolyActor(image_view[1], color=[0.4, 1, 0.6])]
    mark_lists = [[], []]
    text_lists = [[], []]
    pt_radius = 1.5

    mark_boxes = [vmi.TextBox(image_view[0], text='开始配准',
                              size=[0.2, 0.04], pos=[0, 0.08], anchor=[0, 0], pickable=True),
                  vmi.TextBox(image_view[0], text='配准模型',
                              size=[0.2, 0.04], pos=[0, 0.12], anchor=[0, 0], pickable=True)]
    mark_boxes[1].setVisible(False)
    for box in mark_boxes:
        box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

    # 配准视图
    align_view = vmi.View()
    align_view.renderer().SetBackground(0, 0, 0)

    align_model_prop = [vmi.PolyActor(align_view, color=[1, 0.6, 0.4], repres='points'),
                        vmi.PolyActor(align_view, color=[0.4, 1, 0.6], repres='points')]
    align_meal_prop = [vmi.PolyActor(align_view, color=[1, 1, 1]),
                       vmi.PolyActor(align_view, color=[1, 1, 1])]
    align_imp_prop = [vmi.PolyActor(align_view, color=[0.4, 0.6, 1]),
                      vmi.PolyActor(align_view, color=[0.4, 0.6, 1])]

    # 视图布局
    for v in image_view + [align_view]:
        v.setMinimumWidth(round(0.3 * main.screenWidth()))

    main.layout().addWidget(image_view[0], 0, 0, 1, 1)
    main.layout().addWidget(image_view[1], 0, 1, 1, 1)
    main.layout().addWidget(align_view, 0, 2, 1, 1)

    vmi.appexec(main)  # 执行主窗口程序
    vmi.appexit()  # 清理并退出程序
